class Segment:
    def __init__(self, src_port, dst_port, data, seg_type=0, seq=0):
        self.src_port = src_port
        self.dst_port = dst_port
        self.data = data
        self.type = seg_type   # 0 DATA, 1 ACK
        self.seq = seq
        self.length = 9 + len(data)
        self.checksum = self.compute_checksum()

    def compute_checksum(self):
        return sum(str(self.src_port + self.dst_port + self.seq).encode()) + len(self.data)


class Packet:
    def __init__(self, src_ip, dst_ip, payload, ttl=100):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ttl = ttl
        self.protocol = 17
        self.payload = payload


class Frame:
    def __init__(self, src_mac, dst_mac, payload):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.type = "0x0800"
        self.payload = payload