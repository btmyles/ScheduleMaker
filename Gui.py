from tkinter import *
from tkinter import ttk

class Schedule:

    def __init__(self, master):
        self.master = master
        master.title("Schedule Maker")
        master.geometry("800x600+200+150")

        self.term = StringVar()
        self.location = StringVar()

        self.term_lbl = Label(master, text="Term:")
        self.term_lbl.grid(row=0, column=0)

        self.t1 = ttk.Radiobutton(master, text="Summer 2019", variable=self.term, value="2019/SM")
        self.t2 = ttk.Radiobutton(master, text="Fall 2019", variable=self.term, value="2019/FA")
        self.t3 = ttk.Radiobutton(master, text="Winter 2020", variable=self.term, value="2020/WI")
        self.t1.grid(row=0, column=1)
        self.t2.grid(row=1, column=1)
        self.t3.grid(row=2, column=1)

        self.location_lbl = Label(master, text="Location:")
        self.location_lbl.grid(row=4, column=0)

        self.l1 = ttk.Radiobutton(master, text="Saint John", variable=self.location, value="SJ")
        self.l2 = ttk.Radiobutton(master, text="Fredericton", variable=self.location, value="FR")
        self.l1.grid(row=4, column=1)
        self.l2.grid(row=5, column=1)

        self.entry_lbl = Label(master, text="Course IDs:")
        self.entry_lbl.grid(row=7, column=0)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e5 = Entry(master)
        self.e6 = Entry(master)
        self.e1.grid(row=7, column=1)
        self.e2.grid(row=8, column=1)
        self.e3.grid(row=9, column=1)
        self.e4.grid(row=10, column=1)
        self.e5.grid(row=11, column=1)
        self.e6.grid(row=12, column=1)

        self.butt = ttk.Button(master, text="Find Courses", command=self.greet)
        self.butt.grid(row=14, column=0)

        # Set grid spacing
        col_count, row_count = master.grid_size()
        for col in range(col_count):
            master.grid_columnconfigure(col, minsize=20)

        for row in range(row_count):
            master.grid_rowconfigure(row, minsize=20)

    def greet(self):
        print(self.e1.get())

root = Tk()
gui = Schedule(root)
root.mainloop()