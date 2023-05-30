import sys
import tkinter as tk
from tkinter.constants import N, W

def create_widgets(mainframe, files):
    # Create welcome message at the top of the window
    label = tk.Label(mainframe, text="Welcome to cumulative GPA tracker!", bg="lightpink", padx="15", pady="15")
    label.grid(column=0, row=0, sticky=N, columnspan=6)

    semesters = find_semesters(files)
    add_semester_labels(mainframe, semesters)

def find_semesters(files):
    semester_nums = []
    for file in files:
        counter = -5
        semester_num = ""
        while file[counter] != "_":
            semester_num = file[counter] + semester_num
            counter -= 1
        semester_nums.append(semester_num)
    return semester_nums

def add_semester_labels(mainframe, semesters):
    num_rows = 2
    num_columns = len(semesters) // 2
    final_col = 0
    num_semester = len(semesters)

    if len(semesters) % 2 != 0:
        final_col = 1
        num_semester -= 1

    col_tracker = 0
    row_tracker = 0
    sem_tracker = 0

    while sem_tracker < num_semester:
        while num_columns > col_tracker:
            while num_rows > row_tracker:
                sem_label = tk.Label(mainframe, 
                                     text=f"Semester {semesters[sem_tracker]}",
                                     bg="lightpink", padx="15", pady="15")
                sem_label.grid(column=col_tracker, row=1+row_tracker, sticky=W)
                sem_tracker += 1
                row_tracker += 1
            row_tracker = 0
            col_tracker += 1
    if final_col == 1:
        sem_label = tk.Label(mainframe, 
                             text=f"Semester {semesters[sem_tracker]}",
                             bg="lightpink", padx="15", pady="15")
        sem_label.grid(column=col_tracker, row=1, sticky=W)

    
def initialize_gui(files):
    window = tk.Tk()
    window.title("Cumulative GPA tracker")
    window.geometry("+500+200")
    window.configure(background="lightpink")

    mainframe = tk.Frame(window, bg="lightpink")
    mainframe.grid(column=0, row=0, sticky=(N, W))

    create_widgets(mainframe, files)

    window.mainloop()

def main():
    files = sys.argv[1:]
    initialize_gui(files)

if __name__ == "__main__":
    main()
