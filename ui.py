from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from parameters import *
from time import sleep

class App(Tk):
    def __init__(self, width, height, tester, file_handler, data_processor):
        super().__init__()

        self.tester = tester
        self.file_handler = file_handler
        self.data_processor = data_processor

        self.title("NetStab")
        self.geometry(f"{width}x{height}")
        self.running = False

        self.config(menu=Application_menubar(self))
        Ping_frame(self)
        self.status_label = Label(self, text=STATUS_NOT_PINGING_TEXT, font=(UI_FONT, UI_FONT_SIZE))
        self.status_label.pack(padx=UI_X_PADDING, pady=UI_Y_PADDING)
        Data_frame(self)

        self.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.update_idletasks()
        self.update()

    def open_file(self):
        if self.tester.ping_status == True:
            messagebox.showerror("Ping in Progress", ERROR_PING_IN_PROGRESS)
        file_to_open = filedialog.askopenfilename(initialdir="",
                                                  title="Select a File",
                                                  filetypes=(("csv files", "*.csv"), ("All Files", "*.*")))
        if file_to_open:
            if self.file_handler.current_log_file != None:
                self.file_handler.close()
            try:
                self.file_handler.open(file_to_open)
            except Exception as error:
                messagebox.showerror("File Error", f"Unable to open file:\n{error}")
                raise Exception("Unable to open the file provided.")

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            if self.tester.ping_status == True:
                self.status_label.config(text=STATUS_PINGING_TEXT)
            else:
                self.status_label.config(text=STATUS_NOT_PINGING_TEXT)
            self.redraw()
            sleep(.1)
        print("window closed...")

    def close(self):
        self.running = False

class Application_menubar(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="New", command=self.on_new)
        self.file_menu.add_command(label="Open", command=self.on_open)
        self.file_menu.add_command(label="Exit", command=self.on_exit)
        self.add_cascade(label='File',menu=self.file_menu)

        self.help_menu = Menu(self, tearoff=0)
        self.help_menu.add_command(label="Help", command=self.on_help)
        self.add_cascade(label="Help",menu=self.help_menu)

    def on_exit(self):
        self.parent.running = False
    
    def on_new(self):
        self.parent.file_handler.close()
        self.parent.file_handler.new_log()

    def on_open(self):
        try:
            self.parent.open_file()
        except:
            return
        self.parent.file_handler.import_data()
                

    def on_help(self):
        messagebox.showinfo("Helo", HELP_MESSAGE)


class Ping_frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pinging = False
        self.parent = parent
        self.pack(pady=UI_Y_PADDING)

        self.host1_label = Label(self, text="Remote host:", font=(UI_FONT, UI_FONT_SIZE))
        self.host1_label.grid(row=0, column=0, padx=UI_X_PADDING)
        self.host1_entry = Entry(self, width=20, font=(UI_FONT, UI_FONT_SIZE))
        self.host1_entry.insert(0, DEFAULT_HOST)
        self.host1_entry.grid(row=0, column=1, padx=UI_X_PADDING, pady=UI_Y_PADDING)

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

    def ping_button_command(self):
        hosts = self.get_hosts()
        if self.parent.tester.ping_status == True:
            return
        
        if self.parent.file_handler.current_log_file == None:
            messagebox.showerror("No File Open!", ERROR_NO_LOG_FILE)
            return

        if hosts == None:
            messagebox.showerror("User Error!", ERROR_NO_HOSTS)
            return

        num_packets = int(self.num_packets_entry.get())

        self.parent.tester.ping_status = True
        pinging_thread = Thread(target=self.parent.tester.start_pinging, args=(hosts, num_packets, self.parent.file_handler), daemon=True)
        pinging_thread.start()
        self.parent.redraw()

    def stop_button_command(self):
        self.parent.tester.ping_status = False

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
        
class Data_frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(pady=UI_Y_PADDING)

        self.process_button = Button(self, text="Process!", command=self.process_button_command)
        self.process_button.grid(row=0, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)

        self.results_box = Text(self, width=UI_REPORT_WIDTH, height=UI_REPORT_HEIGHT, state='disabled')
        self.set_report_text(REPORT_HEADING + REPORT_SEPARATOR + REPORT_NOT_PROCESSED)
        self.results_box.grid(row=1, column=0, padx=UI_X_PADDING, pady=UI_Y_PADDING)

    def process_button_command(self):
        self.set_report_text(REPORT_WORKING)
        report = self.parent.data_processor.process()
        if report:
            self.set_report_text(REPORT_HEADING + REPORT_SEPARATOR + report)
        else:
            messagebox.showerror(REPORT_ERROR)
            self.set_report_text(REPORT_NOT_PROCESSED)

    def set_report_text(self, text):
        self.results_box.config(state="normal")
        self.results_box.delete("1.0", END)
        self.results_box.insert("1.0", text)
        self.results_box.config(state="disabled")