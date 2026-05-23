# CITS3002 Mini Internet Protocol Stack Simulator

## Overview
This projects goal was to implement a simplified network communication simulator (via Python). Specifically, the simulator models the communication between two hosts through a router. This is to demonstrate the responsibilities within the Transport, Network, and Data Link layers.

The simulator demonstrates the responsibilites through simulating:
- Reliable data transfer using a simplified rdt2.2 style protocol
- Segmentation and reassembly of data
- Packet forwarding through a router
- MAC addressing and frame forwarding
- Routing table lookups
- TTL decrementing
- Checksum computation and verification
- ACK generation and retransmission behaviour

The main output provides a detailed console logging which provides specific information on how data is perceived and moved through the network stack

## File Structure

```txt
.
├── main.py
├── devices.py
├── protocol.py
├── config.py
└── README.md
```
## File Responsibilities

### main.py
- Creates Host A, B, and Router
- Initialises interfaces, MAC tables, and Routing tables
- Reads command line message size input
- Starts communication from Host A to Host B

### devices.py
- Implements Host class
- Implements Router class
- Implements all layer processing (Transport, Data Link, Network)
- ACK Handling and retransmission logic
- Segmentation logic
- Routing table lookup logic

### protocol.py
- Defines protocol data structures such as Segment, Frame, and Packet
- Responsible for checksum operation

### config.py
- Stores constants for all configurations such as:
  - IP Addresses
  - MAC Addresses
  - Router interface addresses
  - TTL defaults
  - Maximum segment size
 
## Protocol Architecture

### Layer 4 - Transport Layer
Responsible for:
- Data segmentation
- Sequence numbering
- ACK generation
- Checksum generation and verification
- Reliable transmission
- Retransmissions
The Transport Layer implementation works on a simplified alternating sequence number bit protocol: 0 -> 1 -> 0 ...

### Layer 3 - Network Layer
Responsible for:
- Packet creation
- IP addressing
- Routing table lookup
- Next-hop determination
- TTL decrementing
- Packet forwarding
Router accesses the routing table to determine things such as next hop and outgoing interface

### Layer 2 - Data Link Layer
Responsible for:
- Frame creation
- MAC addressing
- MAC table lookup
- Frame forwarding
- Frame reception

## Routing table 

In main.py, the router maintains the following routing table: 

```python
routing_table={
    "10.0.1.0/24": {
        "interface": "Interface 1",
        "next_hop": HOST_A_IP
    },
    "10.0.2.0/24": {
        "interface": "Interface 2",
        "next_hop": HOST_B_IP
    }
}
```
The purpose of the routing table is to allow the router to forward packets dynamically based on its subnet.

## Network Topology
The network consists of two hosts (A and B) connected via a router (R1):
Host A  <--->  Router R1  <--->  Host B

Where:

### Host A
- IP: 10.0.1.10
- MAC: AA:AA:AA:AA:AA:AA

### Router Interface 1
- IP: 10.0.1.1
- MAC: BB:BB:BB:BB:BB:BB

### Router Interface 2
- IP: 10.0.2.1
- MAC: CC:CC:CC:CC:CC:CC

### Host B
- IP: 10.0.2.20
- MAC: DD:DD:DD:DD:DD:DD

## Running the program

### Command
python main.py <message_size>

Example:
```python
python main.py 1200
```

## Segmentation behaviour 

Maximum segment size: 500

This means that if data over 500 bytes is sent then it is segmented. E.g 1200 segments into 2, 500 bytes and 1, 200 byte

## Features demonstrated in program
- Encapsulation
- Decapsulation
- Reliable transport
- Router forwarding
- TTL processing
- Routing table lookups
- MAC address resolution
- Frame forwarding
- ACK handling
- Retransmissions

## Error Handling 
The implementation includes:

- Checksum verification
- Incorrect sequence number handling
- Retransmission logic
- TTL expiry detection
- Unknown route handling

