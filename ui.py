from tkinter import *
from helper import *
from constraints import *

class App(Tk):
    def __init__(self, width, height, tester, log_file):
        super().__init__()

        self.tester = tester
        self.log_file = log_file

        self.title("NetStab")
        self.geometry(f"{width}x{height}")
        self.running = False

        self.host_label = Label(self, text="Remote host:", font=(UI_FONT, UI_FONT_SIZE))
        self.host_label.grid(row=0, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.host_entry = Entry(self, width=20, font=(UI_FONT, UI_FONT_SIZE), )
        self.host_entry.insert(0, DEFAULT_HOST)
        self.host_entry.grid(row=0, column=1, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.num_packets_label = Label(self, text="Number of Packets:", font=(UI_FONT, UI_FONT_SIZE))
        self.num_packets_label.grid(row=1, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.num_packets_entry = Entry(self, width=20, font=(UI_FONT, UI_FONT_SIZE))
        self.num_packets_entry.insert(0, DEFAULT_NUM_PACKETS)
        self.num_packets_entry.grid(row=1, column=1, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.ping_button = Button(self, text="Ping!", command=self.ping_button_command)
        self.ping_button.grid(row=3, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)
        self.stop_button = Button(text="Stop!", command=self.stop_button_command)
        self.stop_button.grid(row=3, column=1, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.status_label = Label(self, text=STATUS_NOT_PINGING_TEXT, font=(UI_FONT, UI_FONT_SIZE))
        self.status_label.grid(row=4, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.protocol("WM_DELETE_WINDOW", self.close)
        #app_frame(self)
    
    def change(self):
        self.host_label.config(text="byeee!")

    def ping_button_command(self):
        self.status_label.config(text=STATUS_PINGING_TEXT)
        if int(self.num_packets_entry.get()) == 0:
            self.infinite_ping = True
            while self.infinite_ping == True:
                self.redraw()
                ping_and_write_log(self.host_entry.get(), 1, self.tester, self.log_file)
        else:
            self.redraw()
            ping_and_write_log(self.host_entry.get(), int(self.num_packets_entry.get()), self.tester, self.log_file)
        self.status_label.config(text=STATUS_NOT_PINGING_TEXT)

    def stop_button_command(self):
        self.infinite_ping = False
        self.status_label.config(text=STATUS_STOP_PINGING_TEXT)
        self.redraw()

    def redraw(self):
        self.update_idletasks()
        self.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()
        print("window closed...")

    def close(self):
        self.running = False

class app_frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(pady=20)

        self.button_1 = Button(self, text="Change Button 1")
        self.button_2 = Button(self, text="Change Button 2")
        self.button_3 = Button(self, text="Change Button 3")


        self.button_1.grid(row=0, column=0, padx=0)
        self.button_2.grid(row=0, column=1, padx=0)
        self.button_3.grid(row=0, column=2, padx=100)