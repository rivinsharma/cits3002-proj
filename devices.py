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


class Router:
    def __init__(self, name, interfaces, mac_table, routing_table):
        self.name = name
        self.interfaces = interfaces 
        self.mac_table = mac_table 
        self.routing_table = routing_table 
