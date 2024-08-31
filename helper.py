import time
import datetime
from threading import Thread

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
    for host in hosts:
        threads.append(ThreadWithReturnValue(target=run_ping, args=(host, number, tester)))
    for thread in threads:
        thread.start()
    for thread in threads:
        result = thread.join()
        for packet in result:
            packets.append(packet)
    write_data(packets, logfile)

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
