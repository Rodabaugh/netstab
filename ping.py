import platform
import subprocess
import time

class Tester():
    def __init__(self):
        self.ping_count_flag = "-n" if platform.system().lower()=='windows' else "-c"

    def ping(self, host, packets = 1):
        time_packet_sent = time.time()
        responce = subprocess.check_output(["ping", self.ping_count_flag, "1", host])
        return responce.decode("utf-8").lower(), time_packet_sent

    def parse(self, raw_data, time_packet_sent):
        # system time, ttl, time
        split_lines = raw_data.split("\n")
        del split_lines[0]
        clean_lines = []
        for line in split_lines:
            if not line == '':
                clean_lines.append(line)
            else:
                break 
        
        for line in clean_lines:
            sections = line.split(" ")
            packets = list()
            ttl = None
            latency = None
            for section in sections:
                if "time=" in section:
                    latency = section.strip("time=")
                if "ttl" in section:
                    ttl = section.strip("ttl=")
            if ttl == None:
                packets.append(packet(dropped = True))
            else:
                packets.append(packet(latency, ttl, time_packet_sent))
        return packets
            
            

class packet():
    def __init__(self, latency = None, ttl = None, time_packet_sent = None, dropped = False):
        self.latency = latency
        self.ttl = ttl
        self.time_packet_sent = time_packet_sent
        self.dropped = dropped

    def __repr__(self):
        return f"Latency={self.latency} TTL={self.ttl} Time Sent={self.time_packet_sent} Dropped={self.dropped}"