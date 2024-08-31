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

        Ping_frame(self)

        self.protocol("WM_DELETE_WINDOW", self.close)

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

class Ping_frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(pady=UI_Y_PADDING)

        self.host1_label = Label(self, text="Remote host:", font=(UI_FONT, UI_FONT_SIZE))
        self.host1_label.grid(row=0, column=0, padx=UI_X_PADDING)
        self.host1_entry = Entry(self, width=20, font=(UI_FONT, UI_FONT_SIZE))
        self.host1_entry.insert(0, DEFAULT_HOST)
        self.host1_entry.grid(row=0, column=1, padx=UI_X_PADDING)

        self.host2_label = Label(self, text="Remote host:", font=(UI_FONT, UI_FONT_SIZE))
        self.host2_label.grid(row=1, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)
        self.host2_entry = Entry(self, width=20, font=(UI_FONT, UI_FONT_SIZE))
        self.host2_entry.grid(row=1, column=1, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.host3_label = Label(self, text="Remote host:", font=(UI_FONT, UI_FONT_SIZE))
        self.host3_label.grid(row=2, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)
        self.host3_entry = Entry(self, width=20, font=(UI_FONT, UI_FONT_SIZE))
        self.host3_entry.grid(row=2, column=1, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.num_packets_label = Label(self, text="Number of Packets:", font=(UI_FONT, UI_FONT_SIZE))
        self.num_packets_label.grid(row=3, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)
        self.num_packets_entry = Entry(self, width=20, font=(UI_FONT, UI_FONT_SIZE))
        self.num_packets_entry.insert(0, DEFAULT_NUM_PACKETS)
        self.num_packets_entry.grid(row=3, column=1, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.ping_button = Button(self, text="Ping!", command=self.ping_button_command)
        self.ping_button.grid(row=4, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)
        self.stop_button = Button(self, text="Stop!", command=self.stop_button_command)
        self.stop_button.grid(row=4, column=1, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.status_label = Label(self, text=STATUS_NOT_PINGING_TEXT, font=(UI_FONT, UI_FONT_SIZE))
        self.status_label.grid(row=5, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)

    def ping_button_command(self):
        hosts = self.get_hosts()
        if hosts == None:
            self.status_label.config(text=STATUS_NO_HOSTS)
            return
        self.status_label.config(text=STATUS_PINGING_TEXT)

        # Preform the pinging
        if int(self.num_packets_entry.get()) == 0:
            self.infinite_ping = True
            while self.infinite_ping == True:
                self.parent.redraw()
                ping_and_write_log(hosts, 1, self.parent.tester, self.parent.log_file)
        else:
            for i in range(int(self.num_packets_entry.get())):
                self.parent.redraw()
                ping_and_write_log(hosts, 1, self.parent.tester, self.parent.log_file)
        self.status_label.config(text=STATUS_NOT_PINGING_TEXT)

    def stop_button_command(self):
        self.infinite_ping = False
        self.status_label.config(text=STATUS_STOP_PINGING_TEXT)
        self.parent.redraw()

    def get_hosts(self):
        hosts = list()

        if self.host1_entry.get() != "":
            hosts.append(self.host1_entry.get())
        if self.host2_entry.get() != "":
            hosts.append(self.host2_entry.get())
        if self.host3_entry.get() != "":
            hosts.append(self.host3_entry.get())

        if len(hosts) == 0:
            return None
        else:
            return hosts