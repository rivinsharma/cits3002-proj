from protocol import Segment, Packet, Frame
from config import *

class Host:
    def __init__(self, name, ip, mac, default_gateway_ip, mac_table):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.default_gateway_ip = default_gateway_ip
        self.mac_table = mac_table
        self.expected_seq = 0
        self.received_ack = None
        self.previous_ack = -1

    #This funtion is called from main.py. It starts the process of Host A sending data to Host B.
    def send_data(self, data, destination_ip, router, host):

        print(f"{self.name}: Layer 4: Data received from Application Layer. Data size={len(data)}")

        #Creates a list containing the segements to be sent, maximum segment size is 500. 
        segments = [data[i:i+MAX_SEGMENT_DATA] for i in range(0, len(data), MAX_SEGMENT_DATA)]

        #Loops over the list of segments and sends each one.
        for i, segment_data in enumerate(segments):
            while True:
                segment = Segment(
                    src_port=5000,
                    dst_port=80,
                    data=segment_data,
                    seg_type=0,
                    seq= i%2
                )
                
                #The checksum is constructed in protocol.py when the segment is created.
                print(f"{self.name}: Layer 4: Checksum computed")
                print(f"{self.name}: Layer 4: Segment created by adding transport layer header (DATA, seq={segment.seq})")
                print(f"{self.name}: Layer 4: Segment sent to Network Layer \n")

                packet = Packet(
                    src_ip=self.ip,
                    dst_ip=destination_ip,
                    payload=segment
                )

                print(f"{self.name}: Layer 3: Segment received from Transport Layer: SRC_IP={self.ip}, DST_IP={destination_ip}, TTL={packet.ttl}")
                print(f"{self.name}: Layer 3: Destination IP read: {destination_ip}")
                print(f"{self.name}: Layer 3: Routing table lookup performed")
                print(f"{self.name}: Layer 3: Next-hop IP determined: {self.default_gateway_ip}")
                print(f"{self.name}: Layer 3: Outgoing interface selected")
                print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer \n")

                #Find the next-hop MAC address by using mac table.
                next_hop_mac = self.mac_table[self.default_gateway_ip]

                print(f"{self.name}: Layer 2: Packet received from Network Layer")
                print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({self.default_gateway_ip}) -> {next_hop_mac}")

                frame = Frame(
                    src_mac=self.mac,
                    dst_mac=next_hop_mac,
                    payload=packet
                )

                print(f"{self.name}: Layer 2: Frame created: SRC_MAC={self.mac}, DST_MAC={next_hop_mac}")
                print(f"{self.name}: Layer 2: Frame sent \n")

                #Calls the router's receive_frame function to start the process of sending the frame to Host B.
                router.receive_frame(frame, "Interface 1", host)

                #Checks that the received ACK is correct, before sending the next segment.
                if self.received_ack == i%2:
                    self.previous_ack = self.received_ack
                    break
                else:
                    print(f"{self.name}: Layer 4: No ACK received for seq={segment.seq}. Retransmitting segment \n")
                
    def receive_frame(self, frame, router = None, host = None):
        print(f"{self.name}: Layer 2: Frame received")
        print(f"{self.name}: Layer 2: Source MAC learned: {frame.src_mac}")
        print(f"{self.name}: Layer 2: Packet delivered to Network Layer \n")

        #Calls the receive_packet function to start the process of receiving the packet from the frame.
        self.receive_packet(frame.payload, router, host)
    
    def receive_packet(self, packet, router = None, host = None):
        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dst_ip}, TTL={packet.ttl}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet.dst_ip}")

        #Checks whether the packet is meant for local delivery.
        if packet.dst_ip != self.ip:
            print(f"{self.name}: Layer 3: Packet not meant for this host. Packet discarded \n")
            return
        
        else: 
            print(f"{self.name}: Layer 3: Packet identified as local delivery")

        print(f"{self.name}: Layer 3: Segment delivered to Transport Layer \n")

        segment = packet.payload
        
        print(f"{self.name}: Layer 4: Segment received from Network Layer")

        #Checks whether the checksum is correct.
        if segment.checksum != segment.compute_checksum():
            print(f"{self.name}: Layer 4: Checksum verification failed! Segment discarded")
            return
        
        else:
            print(f"{self.name}: Layer 4: Checksum verified")
        
        #Checks whether segement is an ACK, if an ACK then the next segment (if any) can be sent.
        if segment.type == 1:
            print(f"{self.name}: Layer 4: ACK received: seq={segment.seq}")
            self.received_ack = segment.seq 
            return
        
        #Checks whether the sequence number is correct, then creates an ack segment according to check.
        if segment.seq == self.expected_seq:
            print(f"{self.name}: Layer 4: DATA segment delivered to Application Layer. Data size={len(segment.data)}")
            self.expected_seq = 1 - self.expected_seq
            ack_segment = Segment(
                src_port=segment.dst_port,
                dst_port=segment.src_port,
                data="",
                seg_type=1,
                seq=segment.seq
            ) 
        else:
            print(f"{self.name}: Layer 4: Incorrect DATA segment received (seq={self.previous_ack}). Resending segment.\n")
            ack_segment = Segment(
                src_port=segment.dst_port,
                dst_port=segment.src_port,
                data="",
                seg_type=1,
                seq=previous_ack
            )

        print(f"{self.name}: Layer 4: Segment created by adding transport layer header (ACK, seq={ack_segment.seq})")
        print(f"{self.name}: Layer 4: Segment sent to Network Layer \n")

        #Creation of ACK packet to be sent back to Host A.
        ack_packet = Packet(
            src_ip= self.ip,
            dst_ip= packet.src_ip,
            payload=ack_segment
        )

        print(f"{self.name}: Layer 3: Segment received from Transport Layer: SRC_IP={ack_packet.src_ip}, DST_IP={ack_packet.dst_ip}, TTL={ack_packet.ttl}")
        print(f"{self.name}: Layer 3: Destination IP read: {ack_packet.dst_ip}")
        print(f"{self.name}: Layer 3: Routing table lookup performed")
        print(f"{self.name}: Layer 3: Next-hop IP determined: {self.default_gateway_ip}")
        print(f"{self.name}: Layer 3: Outgoing interface selected")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer \n")

        next_hop_mac = self.mac_table[self.default_gateway_ip]

        print(f"{self.name}: Layer 2: Packet received from Network Layer")
        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({self.default_gateway_ip}) -> {next_hop_mac}")

        #Creation of ACK frame to be sent back to Host A.
        ack_frame = Frame(
            src_mac=self.mac,
            dst_mac=next_hop_mac,
            payload=ack_packet
        )

        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={self.mac}, DST_MAC={next_hop_mac}")
        print(f"{self.name}: Layer 2: Frame sent \n")

        #Calls the router's receive_frame function to start the process of sending the ACK frame back to Host A.
        router.receive_frame(ack_frame, "Interface 2", self)

class Router:
    def __init__(self, name, interfaces, mac_table, routing_table):
        self.name = name
        self.interfaces = interfaces
        self.mac_table = mac_table
        self.routing_table = routing_table

    def receive_frame(self, frame, incoming_interface, host):
        print(f"{self.name}: Layer 2: Frame received on {incoming_interface}")
        print(f"{self.name}: Layer 2: Source MAC learned: {frame.src_mac} on {incoming_interface}")
        print(f"{self.name}: Layer 2: Packet delivered to Network Layer\n")

        packet = frame.payload

        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dst_ip}, TTL={packet.ttl}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet.dst_ip}")

        #Decrements the TTL and checks whether the TTL has expired (reached zero).
        old_ttl = packet.ttl
        packet.ttl -= 1
        if packet.ttl <= 0:
            print(f"{self.name}: Layer 3: TTL expired. Packet discarded \n")
            return

        print(f"{self.name}: Layer 3: TTL decremented: {old_ttl} -> {packet.ttl}")

        print(f"{self.name}: Layer 3: Routing table lookup performed")

        if incoming_interface == "Interface 1":
            next_hop_ip = packet.dst_ip
            next_hop_mac = self.mac_table[next_hop_ip]

            print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop_ip}")
            print(f"{self.name}: Layer 3: Outgoing interface selected (Interface 2)")
            print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer \n")

            print(f"{self.name}: Layer 2: Packet received from Network Layer")
            print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop_ip}) -> {next_hop_mac}")

            new_frame = Frame(
                src_mac=self.interfaces["Interface 2"]["mac"],
                dst_mac=next_hop_mac,
                payload=packet
            )

            print(f"{self.name}: Layer 2: Frame created: SRC_MAC={new_frame.src_mac}, DST_MAC={next_hop_mac}")
            print(f"{self.name}: Layer 2: Frame forwarded on Interface 2 \n")

            #Calls the receive_frame function of Host B to start the process of delivering the packet to Host B.
            host.receive_frame(new_frame, router=self, host=None)

        elif incoming_interface == "Interface 2":
            next_hop_ip = packet.dst_ip
            next_hop_mac = self.mac_table[next_hop_ip]

            print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop_ip}")
            print(f"{self.name}: Layer 3: Outgoing interface selected (Interface 1)")
            print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer \n")

            print(f"{self.name}: Layer 2: Packet received from Network Layer")
            print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop_ip}) -> {next_hop_mac}")

            new_frame = Frame(
                src_mac=self.interfaces["Interface 1"]["mac"],
                dst_mac=next_hop_mac,
                payload=packet
            )

            print(f"{self.name}: Layer 2: Frame created: SRC_MAC={new_frame.src_mac}, DST_MAC={next_hop_mac}")
            print(f"{self.name}: Layer 2: Frame forwarded on Interface 1 \n")

            #Calls the receive_frame function of Host A to start the process of delivering the packet to Host A.
            self.host_a.receive_frame(new_frame, router=self, host=None)