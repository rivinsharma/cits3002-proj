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

    def send_data(self, data, destination_ip, router):
        segment = Segment (
            src_port = 5000,
            dst_port = 80,
            data = data, 
            seg_type = 0, 
            seq = 0
        )
        print(f"{self.name}: Layer 4: Checksum computed")
        print(f"{self.name}: Layer 4: Segment created by adding transport layer header (DATA, seq=0)")
        print(f"{self.name}: Layer 4: Segment sent to Network Layer")
        packet = Packet(
            src_ip = self.ip,
            dst_ip = destination_ip,
            payload = segment
        )
        
        print(f"{self.name}: Layer 3: Segment received from Transport Layer: SRC_IP={self.ip}, DST_IP={destination_ip}, TTL={packet.ttl}")
        print(f"{self.name}: Layer 3: Destination IP read: {destination_ip}")
        print(f"{self.name}: Layer 3: Routing table lookup performed")
        print(f"{self.name}: Layer 3: Next-hop IP determined: {self.default_gateway_ip}")
        print(f"{self.name}: Layer 3: Outgoing interface selected")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")

        next_hop_mac = self.mac_table[self.default_gateway_ip]
        print(f"{self.name}: Layer 2: Packet received from Network Layer")
        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({self.default_gateway_ip}) -> {next_hop_mac}")

        frame = Frame (
            src_mac = self.mac,
            dst_mac = next_hop_mac,
            payload = packet
        )

        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={self.mac}, DST_MAC={next_hop_mac}")
        print(f"{self.name}: Layer 2: Frame sent")

        router.receive_frame(frame, incoming_interface="Interface 1")
    
    def receive_frame(self, frame):
        print(f"{self.name}: Layer 2: Frame received")
        print(f"{self.name}: Layer 2: Source MAC learned: {frame.src_mac}")
        print(f"{self.name}: Layer 2: Packet delivered to Network Layer")

class Router:
    def __init__(self, name, interfaces, mac_table, routing_table):
        self.name = name
        self.interfaces = interfaces 
        self.mac_table = mac_table 
        self.routing_table = routing_table 


    def receive_frame(self, frame, incoming_interface):
        print(f"{self.name}: Layer 2: Frame received on {incoming_interface}")
        print(f"{self.name}: Layer 2: Source MAC learned: {frame.src_mac} on {incoming_interface}")
        print(f"{self.name}: Layer 2: Packet delivered to Network Layer")

        packet = frame.payload

        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dst_ip}, TTL={packet.ttl}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet.dst_ip}")

        old_ttl = packet.ttl
        packet.ttl -= 1
        print(f"{self.name}: Layer 3: TTL decremented: {old_ttl} -> {packet.ttl}")

        print(f"{self.name}: Layer 3: Routing table lookup performed")

        next_hop_ip = host_b.ip
        next_hop_mac = HOST_B_MAC

        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop_ip}")
        print(f"{self.name}: Layer 3: Outgoing interface selected (Interface 2)")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")

        print(f"{self.name}: Layer 2: Packet received from Network Layer")
        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop_ip}) -> {next_hop_mac}")
        new_frame = Frame(
            src_mac=R1_IF2_MAC,
            dst_mac=next_hop_mac,
            payload=packet
        )

        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={R1_IF2_MAC}, DST_MAC={next_hop_mac}")
        print(f"{self.name}: Layer 2: Frame forwarded on Interface 2")

        host_b.receive_frame(new_frame)