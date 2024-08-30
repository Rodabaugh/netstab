import time
import datetime
from ping import *
from ui import *

def main():
    log_name = "NetStab " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S') + ".csv"
    log_file = open(log_name,"w")
    log_file.write("Time Sent,Host,Latency,TTL,Dropped\n")

    tester = Tester()
    main_window = App(800, 600, tester, log_file)        

    main_window.wait_for_close()
    log_file.close()

main()