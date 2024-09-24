from parameters import *

class Data_processor():
    def __init__(self):
        self.processing_status = False
        self.current_data = list()

    def process(self):
        report = ""
        lowest = self.process_lowest_latency()
        average = self.process_average()
        highest = self.process_highest_latency()
        drop_count = self.count_dropped()
        highest_drop_counts = self.highest_sequential_dropped()
        highest_not_dropped_counts = self.highest_sequential_not_dropped()

        report += REPORT_LOWEST_LATENCY

        for host in lowest:
            report += str(host) + " - " + str(lowest[host]) + "\n"

        report += REPORT_AVERAGE_HEADING
        
        for host in average:
            report += str(host) + " - " + str(round(average[host], 2)) + "\n"

        report += REPORT_HIGHEST_LATENCY

        for host in highest:
            report += str(host) + " - " + str(highest[host]) + "\n"
        
        report += REPORT_DROPPED_HEADING
        for host in drop_count:
            report += str(host) + " - " + str(drop_count[host]) + " dropped\n"

        report += REPORT_HIGHEST_SEQUENTIAL_DROPPED
        for host in highest_drop_counts:
            report += str(host) + " - " + str(highest_drop_counts[host]) + " dropped in a row\n"

        report += REPORT_HIGHEST_SEQUENTIAL_NOT_DROPPED
        for host in highest_not_dropped_counts:
            report += str(host) + " - " + str(highest_not_dropped_counts[host]) + " in a row were not dropped\n"

        return report

    def count_dropped(self):
        dropped_packets = {}
        for packet in self.current_data:
            if packet.dropped == True:
                if packet.host not in dropped_packets:
                    dropped_packets[packet.host] = 1
                else:
                    dropped_packets[packet.host] += 1
        return dropped_packets
    
    def process_lowest_latency(self):
        lowest = self.get_hosts()
        for host in lowest:
            lowest[host] = float("inf")
        for packet in self.current_data:
            if packet.dropped == False:
                if float(packet.latency) < lowest[packet.host]:
                    lowest[packet.host] = float(packet.latency)
        return lowest

    def process_average(self):
        hosts = self.get_hosts()

        for host in hosts:
            hosts[host] = list()
        for packet in self.current_data:
            if packet.dropped == False:
                hosts[packet.host].append(packet.latency)

        latency = {}
        for host in hosts:
            if len(hosts[host]) != 0:
                sum = 0
                packet_latencies = hosts.get(host)
                for packet_latency in packet_latencies:
                    sum += float(packet_latency)
                    latency[host] = sum / len(packet_latencies)
        return latency
    
    def process_highest_latency(self):
        highest = self.get_hosts()
        for host in highest:
            highest[host] = float("-inf")
        for packet in self.current_data:
            if packet.dropped == False:
                if float(packet.latency) > highest[packet.host]:
                    highest[packet.host] = float(packet.latency)
        for host in highest:
            if highest[host] == float("-inf"):
                highest[host] = float("inf")
        return highest
    
    def highest_sequential_dropped(self):
        highest_drop_counts = self.get_hosts()
        for host in highest_drop_counts:
            highest_drop_counts[host] = 0
            current = 0
            for packet in self.current_data:
                if packet.host == host:
                    if packet.dropped == True:
                        current += 1
                    elif packet.dropped == False:
                        if current > highest_drop_counts[host]:
                            highest_drop_counts[host] = current
                        current = 0
            if current != 0:
                highest_drop_counts[host] = current
        return highest_drop_counts
    
    def highest_sequential_not_dropped(self):
        highest_not_dropped_count = self.get_hosts()
        for host in highest_not_dropped_count:
            highest_not_dropped_count[host] = 0
            current = 0
            for packet in self.current_data:
                if packet.host == host:
                    if packet.dropped == False:
                        current += 1
                    elif packet.dropped == True:
                        if current > highest_not_dropped_count[host]:
                            highest_not_dropped_count[host] = current
                        current = 0
            if current != 0:
                highest_not_dropped_count[host] = current
        return highest_not_dropped_count

    def get_hosts(self):
        hosts = {}
        for packet in self.current_data:
            if packet.host not in hosts:
                hosts[packet.host] = None
        return hosts

    def add_packets(self, packets):
        for packet in packets:
            self.current_data.append(packet)

    def clear(self):
        self.current_data = list()

    def get_packets(self):
        return self.current_data