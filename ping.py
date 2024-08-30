import platform
import subprocess
import time

class Tester():
    def __init__(self):
        self.ping_count_flag = "-n" if platform.system().lower()=='windows' else "-c"

    def ping(self, host, packets = 1):
        time_packet_sent = time.time()
        responce = subprocess.run(["ping", self.ping_count_flag, "1", host], stdout = subprocess.PIPE, check=False)
        return responce.stdout.decode("utf-8").lower(), responce.returncode, time_packet_sent

    def parse(self, raw_data, returncode, time_packet_sent, host):
        # system time, ttl, time
        packets = list()

        if returncode == 1:
            packets.append(packet(host, None, None, time_packet_sent, dropped=True))
            print("Dropped...")
            return packets
        else:
            if platform.system().lower() == "windows":
                split_lines = raw_data.split("\r\n")
            else:
                split_lines = raw_data.split("\n")
            del split_lines[0]
            if platform.system().lower() == "windows":
                del split_lines[0]
            clean_lines = []

            for line in split_lines:
                print(line)
                if not line == '':
                    clean_lines.append(line)
                if "ping statistics" in line:
                    break
                else:
                    break 
            
            for line in clean_lines:
                sections = line.split(" ")
                ttl = None
                latency = None
                for section in sections:
                    if "time=" in section:
                        latency = section.strip("time=")
                    if "ttl" in section:
                        ttl = section.strip("ttl=")
                if ttl == None:
                    packets.append(packet(host, dropped = True))
                else:
                    packets.append(packet(host, latency, ttl, time_packet_sent))
            return packets

class packet():
    def __init__(self, host, latency = None, ttl = None, time_packet_sent = None, dropped = False):
        self.host = host
        self.latency = latency
        self.ttl = ttl
        self.time_packet_sent = time_packet_sent
        self.dropped = dropped

    def __repr__(self):
        return f"Host={self.host} Latency={self.latency} TTL={self.ttl} Time Sent={self.time_packet_sent} Dropped={self.dropped}"