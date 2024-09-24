import time
import datetime
import calendar
from ping import packet
from parameters import *

class File_handler():
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.current_log_file = None
        self.new_log()

    def write_data(self, packets):
        for packet in packets:
            gm_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(packet.time_packet_sent))
            self.current_log_file.writelines(f"{gm_time},{packet.host},{packet.latency},{packet.ttl},{packet.dropped}\n")

    def new_log(self):
        log_name = DEFAULT_LOG_DIR + "NetStab " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S') + ".csv"
        self.current_log_file = open(log_name,"w")
        self.current_log_file.write(FILE_HEADING)
        self.data_processor.clear()
    
    def close(self):
        self.data_processor.clear()
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
                epoch_time = calendar.timegm(time.strptime(elements[0], '%Y-%m-%d %H-%M-%S'))

                if elements[4] == "False":
                    dropped = False
                else:
                    dropped = True

                packets.append(packet(elements[1], elements[2], elements[3], epoch_time, dropped))
        self.data_processor.clear()
        self.data_processor.add_packets(packets)