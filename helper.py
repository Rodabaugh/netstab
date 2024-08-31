import time
import datetime
import concurrent.futures

def run_ping(host, number, tester):
    packets = list()
    for _ in range(number):
        ping = tester.ping(host)
        packets.append(tester.parse(ping[0], ping[1], ping[2], host).pop())
        time.sleep(1)
    return packets

def write_data(packets, log_file):
    for packet in packets:
        local_time = datetime.datetime.fromtimestamp(packet.time_packet_sent).strftime('%Y-%m-%d %H:%M:%S')
        log_file.writelines(f"{local_time},{packet.host},{packet.latency},{packet.ttl},{packet.dropped}\n")

def ping_and_write_log(hosts, number, tester, logfile):
    packets = list()
    threads = list()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(run_ping, host, number, tester) for host in hosts]

        for f in concurrent.futures.as_completed(results):
            for packet in f.result():
                packets.append(packet)
    write_data(packets, logfile)