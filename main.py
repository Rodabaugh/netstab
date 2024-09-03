from ping import *
from files import *
from processor import *
from ui import *
from parameters import *

def main():
    data_procesor = Data_processor()
    file_handler = File_handler(data_procesor)
    tester = Tester(data_procesor)
    main_window = App(UI_WIDTH, UI_HEIGHT, tester, file_handler, data_procesor)        

    main_window.wait_for_close()
    if file_handler.current_log_file != None:
        file_handler.close()

main()