import time
import datetime

class File_handler():
    def __init__(self):
        self.new_log()
        
    def write_data(self, packets):
        for packet in packets:
            local_time = datetime.datetime.fromtimestamp(packet.time_packet_sent).strftime('%Y-%m-%d %H:%M:%S')
            self.current_log_file.writelines(f"{local_time},{packet.host},{packet.latency},{packet.ttl},{packet.dropped}\n")

    def new_log(self):
        log_name = "NetStab " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S') + ".csv"
        self.current_log_file = open(log_name,"w")
        self.current_log_file.write("Time Sent,Host,Latency,TTL,Dropped\n")
    
    def close(self):
        self.current_log_file.close()
        
    