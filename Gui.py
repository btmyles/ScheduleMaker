#! ./env/bin/python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import ScheduleMaker

class Schedule:

    def __init__(self, master):
        self.master = master
        master.title("Schedule Maker")
        master.geometry("800x600+200+150")

        # Instance variables
        self.term = StringVar()
        self.location = StringVar()
        self.term_selected = False
        self.location_selected = False

        # Term
        self.term_lbl = Label(master, text="Term:")
        self.term_lbl.grid(row=0, column=0, sticky=W)

        self.t1 = ttk.Radiobutton(master, text="Summer 2019", variable=self.term, command=self.t_selected, value="2019/SM")
        self.t2 = ttk.Radiobutton(master, text="Fall 2019", variable=self.term, command=self.t_selected, value="2019/FA")
        self.t3 = ttk.Radiobutton(master, text="Winter 2020", variable=self.term, command=self.t_selected, value="2020/WI")
        self.t1.grid(row=0, column=1, sticky=W)
        self.t2.grid(row=1, column=1, sticky=W)
        self.t3.grid(row=2, column=1, sticky=W)

        # Location
        self.location_lbl = Label(master, text="Location:")
        self.location_lbl.grid(row=4, column=0, sticky=W)

        self.l1 = ttk.Radiobutton(master, text="Saint John", variable=self.location, command=self.l_selected, value="SJ")
        self.l2 = ttk.Radiobutton(master, text="Fredericton", variable=self.location, command=self.l_selected, value="FR")
        self.l1.grid(row=4, column=1, sticky=W)
        self.l2.grid(row=5, column=1, sticky=W)

        # Course names
        self.entry_lbl = Label(master, text="Course IDs:")
        self.entry_lbl.grid(row=7, column=0, sticky=W)

        self.entries = []
        for i in range(6):
            self.entries.append(Entry(master))
            self.entries[i].grid(row=i+7, column=1, sticky=W)

        # Schedule Button
        self.butt = ttk.Button(master, text="Find Courses", command=self.run)
        self.butt.grid(row=14, column=0, sticky=W)

        # Output
        self.output = Text(master)
        self.output.grid(row=2, column=3, rowspan=12, columnspan=3)
        self.output.config(state=DISABLED)

        # Set grid spacing
        col_count, row_count = master.grid_size()
        for col in range(col_count):
            master.grid_columnconfigure(col, minsize=20)

        for row in range(row_count):
            master.grid_rowconfigure(row, minsize=20)

    def output_text(self, out):
        self.output.config(state=NORMAL)
        self.output.insert(END, out)
        self.output.config(state=DISABLED)

    def t_selected(self):
        self.term_selected = True

    def l_selected(self):
        self.location_selected = True

    def run(self):
        # Verify that a term and location have been selected
        if not self.term_selected:
            messagebox.showerror("Error", "Select a term")
        elif not self.location_selected:
            messagebox.showerror("Error", "Select a location")
        else:
            # Get input from each widget and run schedule finder function
            value_entered = False
            for entry in self.entries:
                if entry.get() != "":
                    value_entered = True
                    time = ScheduleMaker.get_schedule(self.term.get(), 'UG', entry.get(), self.location.get())
                    self.output_text(time)
            # Validate that a course has been entered
            if not value_entered:
                messagebox.showerror("Error", "Enter at least one course")
root = Tk()
gui = Schedule(root)
root.mainloop()
