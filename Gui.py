from tkinter import *

class Schedule:
    def __init__(self, master):
        self.master = master
        master.title("Schedule Maker")
        master.geometry("800x600+200+150")

        self.term_lbl = Label(master, text="Term:")
        self.term_lbl.grid(row=0, column=0)

        self.location_lbl = Label(master, text="Location:")
        self.location_lbl.grid(row=2, column=0)

        self.entry_lbl = Label(master, text="Course IDs between spaces:")
        self.entry_lbl.grid(row=4, column=0)


        self.butt = Button(master, text="Find Courses", command=self.greet)
        self.butt.grid(row=5, column=0)

        # Set grid spacing
        col_count, row_count = master.grid_size()
        for col in range(col_count):
            master.grid_columnconfigure(col, minsize=20)

        for row in range(row_count):
            master.grid_rowconfigure(row, minsize=20)

    def greet(self):
        print("Hello there")


root = Tk()
gui = Schedule(root)
root.mainloop()