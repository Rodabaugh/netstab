from ping import *
from files import *
from processor import *
from ui import *

def main():
    data_procesor = Data_processor()
    file_handler = File_handler(data_procesor)
    tester = Tester(data_procesor)
    main_window = App(800, 600, tester, file_handler, data_procesor)        

    main_window.wait_for_close()
    file_handler.close()

main()