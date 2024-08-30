import time
import datetime

def run_ping(host, number, tester):
    packets = list()
    for x in range(number):
        ping = tester.ping(host)
        packets.append(tester.parse(ping[0], ping[1], ping[2], host).pop())
        time.sleep(1)
    return packets

def write_data(packets, log_file):
    for packet in packets:
        local_time = datetime.datetime.fromtimestamp(packet.time_packet_sent).strftime('%Y-%m-%d %H:%M:%S')
        log_file.writelines(f"{local_time},{packet.host},{packet.latency},{packet.ttl},{packet.dropped}\n")

def ping_and_write_log(host, number, tester, logfile):
    packets = run_ping(host, number, tester)
    write_data(packets, logfile)