from ping import *
from files import *
from ui import *

def main():
    file_handler = File_handler()
    tester = Tester()
    main_window = App(800, 600, tester, file_handler)        

    main_window.wait_for_close()
    file_handler.close()

main()