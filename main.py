import time
import datetime
from ping import *

tester = Tester()
log_name = "NetStab " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S') + ".csv"

log_file = open(log_name,"w")

log_file.write("Time Sent,Latency,TTL,Dropped\n")

for x in range(3):
    ping = tester.ping("1.1.1.1")
    packets = tester.parse(ping[0], ping[1], ping[2])
    for packet in packets:
        print(packet)
        local_time = datetime.datetime.fromtimestamp(packet.time_packet_sent).strftime('%Y-%m-%d %H:%M:%S')
        log_file.writelines(f"{local_time},{packet.latency},{packet.ttl},{packet.dropped}\n")
    time.sleep(1)

log_file.close()