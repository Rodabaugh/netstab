import platform
import subprocess
import time
import concurrent.futures

class Tester():
    def __init__(self, data_processor):
        self.ping_count_flag = "-n" if platform.system().lower()=='windows' else "-c"
        self.data_processor = data_processor
        self.ping_status = False

    def ping(self, host, packets = 1):
        time_packet_sent = time.time()
        response = subprocess.run(["ping", self.ping_count_flag, "1", host], stdout = subprocess.PIPE, check=False)
        return response.stdout.decode("utf-8").lower(), response.returncode, time_packet_sent
    
    def start_pinging(self, hosts, num_packets, file_handler):
        self.ping_status = True
        if num_packets == 0:
            while self.ping_status == True:
                self.ping_and_write_log(hosts, 1, file_handler)
        else:
            for i in range(num_packets):
                if self.ping_status == False:
                    return
                self.ping_and_write_log(hosts, 1, file_handler)
            self.ping_status = False

    def run_ping(self,host, number):
        packets = list()
        for _ in range(number):
            ping = self.ping(host)
            packets.append(self.parse(ping[0], ping[1], ping[2], host).pop())
            time.sleep(1)
        return packets

    def ping_and_write_log(self, hosts, number, file_handler):
        packets = list()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.run_ping, host, number) for host in hosts]

            for f in concurrent.futures.as_completed(results):
                for packet in f.result():
                    packets.append(packet)
        file_handler.write_data(packets)
        self.data_processor.add_packets(packets)
        return packets

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
                        latency = latency.strip("ms")
                    if "ttl" in section:
                        ttl = section.strip("ttl=")
                if ttl == None:
                    packets.append(packet(host, dropped = True))
                else:
                    packets.append(packet(host, latency, ttl, time_packet_sent))
            return packets

class packet():
    def __init__(self, host, latency = None, ttl = None, time_packet_sent = None, dropped = False): 
        self.host = str(host)
        self.latency = latency
        self.ttl = ttl
        self.time_packet_sent = time_packet_sent
        self.dropped = bool(dropped)

    def __repr__(self):
        return f"[Host={self.host} Latency={self.latency} TTL={self.ttl} Time Sent={self.time_packet_sent} Dropped={self.dropped}]"