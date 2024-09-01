import time
import datetime
import calendar
from ping import packet
from constraints import *

class File_handler():
    def __init__(self, data_procesor):
        self.data_procesor = data_procesor
        self.current_log_file = None
        self.new_log()

    def write_data(self, packets):
        for packet in packets:
            local_time = datetime.datetime.fromtimestamp(packet.time_packet_sent).strftime('%Y-%m-%d %H:%M:%S')
            local_time += " " + str(datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo)
            self.current_log_file.writelines(f"{local_time},{packet.host},{packet.latency},{packet.ttl},{packet.dropped}\n")

    def new_log(self):
        log_name = "NetStab " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S') + ".csv"
        self.current_log_file = open(log_name,"w")
        self.current_log_file.write(FILE_HEADING)
    
    def close(self):
        self.current_log_file.close()
        self.current_log_file = None
        self.log_file_contents = None

    def open(self, file_to_open):
        if self.current_log_file != None:
            self.close()
        try:
            print(f"Opening file: {file_to_open}")
            self.current_log_file = open(file_to_open, "r+")
        except Exception as error:
            print(f"I failed: {error}")

        self.raw_data = self.current_log_file.read().split("\n")
        
        if self.raw_data[0]+"\n" != FILE_HEADING:
            self.close()
            raise Exception(f"File {file_to_open} is not a netstab file.")
        
    def import_data(self):
        packets = list()
        for line in self.raw_data:
            if line+"\n" != FILE_HEADING and line != "":
                elements = line.split(",")
                local_time = time.strptime(elements[0], "%Y-%m-%d %H:%M:%S %Z")
                epoch_time = calendar.timegm(local_time)
                packets.append(packet(elements[1], elements[2], elements[3], epoch_time, elements[4]))
        self.data_procesor.add_packets(packets)
        print(self.data_procesor.get_packets())