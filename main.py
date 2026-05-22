from devices import Host, Router
from config import *

import sys

message_size = int(sys.argv[1])

data = "X" * message_size


host_a = Host(
    name="Host A",
    ip=HOST_A_IP,
    mac=HOST_A_MAC,
    default_gateway_ip=R1_IF1_IP,
    mac_table={
        R1_IF1_IP: R1_IF1_MAC
    }
)

host_b = Host(
    name="Host B",
    ip=HOST_B_IP,
    mac=HOST_B_MAC,
    default_gateway_ip=R1_IF2_IP,
    mac_table={
            R1_IF2_IP: R1_IF2_MAC
    }
)

router = Router(
    name="Router R1",
    interfaces={},
    mac_table={},
    routing_table={}
)

host_a.send_data(data, HOST_B_IP, router, host_b)