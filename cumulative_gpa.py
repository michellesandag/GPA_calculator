import sys
import tkinter as tk
from tkinter.constants import N, W, E, S
from tkinter import ttk
import csv

def create_widgets(mainframe, files, username):
    # Create welcome message at the top of the window
    label = tk.Label(mainframe, text="Welcome to cumulative GPA tracker!",
                     bg="lightpink", padx="15", pady="15")
    label.grid(column=0, row=0, sticky=N, columnspan=6)
    user_label = tk.Label(mainframe, text=f"Data for user {username}:", 
                          bg="lightpink", padx="15", pady="5")
    user_label.grid(column=0, row=1, sticky=W, columnspan=6)

    semesters = find_semesters(files)
    all_data = []
    add_semester_labels(mainframe, semesters, username, all_data)

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

def add_semester_labels(mainframe, semesters, username, all_data):
    num_rows = 8
    num_columns = len(semesters) // 2 + 1
    final_col = 0
    num_semester = len(semesters)

    if len(semesters) % 2 != 0:
        final_col = 1
        num_semester -= 1

    col_tracker = 1
    row_tracker = 2
    sem_tracker = 0
    avg_all_gpa = []
    
    empty_label = tk.Label(mainframe, 
                         text=" ",
                         bg="lightpink", padx="15", pady="15")
    empty_label.grid(column=0, row=2, sticky=W)
    empty_label_2 = tk.Label(mainframe, 
                         text=" ",
                         bg="lightpink", padx="15", pady="15")
    empty_label_2.grid(column=0, row=3, sticky=W)

    while sem_tracker < num_semester & num_columns > col_tracker:
        while num_rows > row_tracker:
            avg_gpa = get_avg_gpa(sem_tracker+1, username, avg_all_gpa)
            label_text = f"Semester {semesters[sem_tracker]}: "
            label_text += f"Average of {avg_gpa}"
            sem_label = tk.Label(mainframe, text=label_text,
                                 bg="lightpink", padx="15", pady="5")
            sem_label.grid(column=col_tracker, row=row_tracker, sticky=W)
            sem_table = add_sem_table(mainframe, semesters, 
                                      col_tracker, row_tracker)
            fill_sem_table(sem_table, sem_tracker+1, username, all_data)
            cumul_gpa = sum(avg_all_gpa) / len(avg_all_gpa)
            sem_gpa_label = tk.Label(mainframe, text=f"Cumulative GPA: {cumul_gpa}",
                                 bg="lightpink", pady="5")
            sem_gpa_label.grid(column=col_tracker, row=row_tracker+2, sticky=W)
            sem_tracker += 1
            row_tracker += 4
            
        row_tracker = 2
        col_tracker += 2

    if final_col == 1:
        avg_gpa = get_avg_gpa(sem_tracker+1, username, avg_all_gpa)
        label_text = f"Semester {semesters[sem_tracker]}: "
        label_text += f"Average of {avg_gpa}"
        sem_label = tk.Label(mainframe, text=label_text,
                             bg="lightpink", padx="15", pady="5")
        sem_label.grid(column=col_tracker, row=2, sticky=W)
        
        cumul_gpa = sum(avg_all_gpa) / len(avg_all_gpa)
        sem_gpa_label = tk.Label(mainframe, text=f"Cumulative GPA: {cumul_gpa}",
                             bg="lightpink", pady="5")
        sem_gpa_label.grid(column=col_tracker, row=4, sticky=W)
        sem_table = add_sem_table(mainframe, semesters, col_tracker, 2)
        fill_sem_table(sem_table, sem_tracker+1, username, all_data)


def get_avg_gpa(sem_tracker, username, avg_all_gpa):
    
    filename = username + "_semester_" + str(sem_tracker) + ".csv"
    with open(filename,'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for (i,row) in enumerate(csv_reader):
            if i == 0: # If file is empty
                pass # Throw exception
    csv_file.close()
    avg_all_gpa.append(float(row[-2]))
    return row[-2]

def fill_sem_table(sem_table, sem_tracker, username, all_data):
    
    sem_class_names = []
    sem_class_nums = []
    sem_gpa_points = []
    sem_credits = []
    sem_desigs = []
    
    filename = username + "_semester_" + str(sem_tracker) + ".csv"
    with open(filename,'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for (i,row) in enumerate(csv_reader):
            if i == 0: # If file is empty
                pass # Throw exception
            elif row[0] == "Average Grade":
                break
            else: 
                sem_class_names.append(row[0])
                sem_class_nums.append(row[1])
                sem_gpa_points.append(row[2])
                sem_credits.append(row[3])
                sem_desigs.append(row[4])
                
    csv_file.close()
    
    for j in range(len(sem_class_names)):
        sem_table.insert('', 'end', values=(sem_class_names[j], sem_desigs[j],
                                            sem_credits[j], sem_gpa_points[j]))
    all_data.append([sem_class_names, sem_class_names, sem_class_nums, 
                    sem_gpa_points, sem_desigs, sem_credits])

def add_sem_table(mainframe, semesters, col_tracker, row_tracker):
    
    treeview = ttk.Treeview(mainframe, 
                            columns=('Class Name', 'Desig.', 
                                     'Credits', 'GPA Points',), 
                            show='headings')
    treeview.column('Class Name', width=150) 
    treeview.heading('Class Name', text='Class Name')
    treeview.column('GPA Points', width=70)
    treeview.heading('GPA Points', text='GPA Points')
    treeview.column('Desig.', width=40)
    treeview.heading('Desig.', text='Desig.')
    treeview.column('Credits', width=40)
    treeview.heading('Credits', text='Credits')
    
    sem_label = tk.Label(mainframe, text=" ",
                         bg="lightpink", padx="15", pady="15")
    sem_label.grid(column=col_tracker+1, row=row_tracker+1, sticky=W)
    
    treeview.grid(column=col_tracker, row=row_tracker+1, sticky=E)
    return treeview
    
def initialize_gui(files, username):
    window = tk.Tk()
    window.title("Cumulative GPA tracker")
    window.geometry("+500+200")
    window.configure(background="lightpink")

    mainframe = tk.Frame(window, bg="lightpink")
    mainframe.grid(column=0, row=0, sticky=(N, W))

    create_widgets(mainframe, files, username)

    window.mainloop()

def main():
    username = sys.argv[1]
    files = sys.argv[2:]
    initialize_gui(files, username)

if __name__ == "__main__":
    main()
