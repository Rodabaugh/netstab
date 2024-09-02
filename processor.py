from parameters import *

class Data_processor():
    def __init__(self):
        self.processing_status = False
        self.current_data = list()

    def process(self):
        print(self.get_packets())
        average = self.process_average()
        drop_count = self.count_dropped()

        print(average)
        print(drop_count)

    def count_dropped(self):
        dropped_packets = {}
        for packet in self.current_data:
            if packet.dropped == True:
                print(packet)
                if packet.host not in dropped_packets:
                    dropped_packets[packet.host] = 1
                else:
                    dropped_packets[packet.host] += 1
        return dropped_packets

    def process_average(self):
        hosts = self.get_hosts()
        for packet in self.current_data:
            if packet.dropped == False:
                hosts[packet.host].append(packet.latency)
                print(packet)

        latency = {}
        for host in hosts:
            if len(hosts[host]) != 0:
                sum = 0
                packet_latencies = hosts.get(host)
                for packet_latency in packet_latencies:
                    sum += float(packet_latency)
                    latency[host] = sum / len(packet_latencies)
        return latency
    
    def get_hosts(self):
        hosts = {}
        for packet in self.current_data:
            if packet.host not in hosts:
                hosts[packet.host] = list()
        return hosts

    def add_packets(self, packets):
        for packet in packets:
            self.current_data.append(packet)

    def clear(self):
        self.current_data = list()

    def get_packets(self):
        return self.current_data