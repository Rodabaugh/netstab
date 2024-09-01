from constraints import *

class Data_processor():
    def __init__(self):
        self.processing_status = False
        self.current_data = list()

    def process(self):
        #Time Sent,Host,Latency,TTL,Dropped
        print(self.current_data)

    def add_packets(self, packets):
        for packet in packets:
            self.current_data.append(packet)

    def get_packets(self):
        return self.current_data