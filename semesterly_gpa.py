#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed May 24 20:57:05 2023

My preliminary GPA calculator code

@author: michellesandag
"""

from tkinter import *
from tkinter import ttk
import csv
from functools import partial

# Defining the add command (user adds their grade for a class)
def add():
    class_name_val = class_name.get()
    grade_val = grade.get()
    credit_val = credit.get()
    all_credits.append(float(credit_val))
    gpa_points = float(find_gpa(grade_val)) * float(credit_val)
    all_gpa_points.append(gpa_points)
    gpa_val = find_gpa(grade_val)
    checks = [(H_check, "H"), (S_check, "S"), (N_check, "N"), (Q_check, "Q"), (E_check, "E"), (W_check, "W")]

    # Iterate over the checkbuttons and set their values
    for check, label in checks:
        if check.get() == "1":
            check.set(label)
        else:
            check.set("")
            
    desig_val = H_check.get() + S_check.get() + N_check.get() + Q_check.get()
    desig_val += E_check.get() + W_check.get()
    all_desigs.append(desig_val)
    if class_name_val and grade_val:
        gpa_dict[class_name_val] = grade_val
        treeview.insert('', 'end', 
                        values=(class_name_val, desig_val, grade_val, gpa_points))
        class_name.set("")
        grade.set('')
        credit.set('')
        
        # Recalculate average GPA and letter grade
        average_gpa = calculate_average_gpa()
        average_grade = find_letter(average_gpa)
        
        # Update the average GPA and letter grade labels
        str_average_gpa.set(f"{average_gpa:.2f}")
        str_average_grade.set(average_grade)

# Define function to calculate average GPA
def calculate_average_gpa():
    if sum(all_credits)== 0:
        return 0
    else:
        return sum(all_gpa_points)/sum(all_credits)
        

# Define function for finding GPA given a letter grade
def find_gpa(letter_grade):
    gpa_letter = {
        "A+": 4.0, "A": 4.0, "A-": 3.7, 
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7
    }
    return str(gpa_letter[letter_grade])

# Define function for finding letter grade given a GPA
def find_letter(gpa):
    gpa_letter = {
        "A+": 4.0, "A": 4.0, "A-": 3.7, 
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7
    }
    
    for key, value in gpa_letter.items():
        if gpa == value:
            return key  
        if gpa < value:
            continue
        if gpa > value:
            return key
            
def export(semester_number):
    semesterfile = f"semester_{semester_number}_data.csv"
    with open(semesterfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        all_data = []
        counter = 0
        for class_name, grade in gpa_dict.items():
            all_data.append([class_name, grade, all_gpa_points[counter], 
                            all_credits[counter], all_desigs[counter]])
            counter += 1

        # Write the data to the CSV file
        writer.writerow(['Class Name', 'Grade', 'GPA Points', 'Credits', 'Designation'])
        writer.writerows(all_data)
        writer.writerow(['Average Grade', str_average_grade.get(),'Average GPA', str_average_gpa.get(), '-'])

def save():
    # Open a new window
    save_window = Toplevel(window)
    save_window.geometry("270x130+570+300")
    save_window.title("Semester Data Entry")
    saveframe = ttk.Frame(save_window, padding="5 5 7 7")
    saveframe.grid(column=0, row=0, sticky=(N, W, E, S))

    # Ask user to input semester number
    save_label = ttk.Label(saveframe, text="Please enter which semester the \npreviously entered data corresponds to", style="Custom.TLabel")
    save_label.grid(column=0, row=0, sticky=N, columnspan=2)
    semester_label = ttk.Label(save_window, text="Semester #", style="LeftPadded.TLabel").grid(column=0, row=1, sticky=W)

    semester = StringVar()
    semester_entry = ttk.Entry(save_window, width=10, textvariable=semester)
    semester_entry.grid(column=0, row=1, sticky=E)
    semester_entry.focus()

    export_command = lambda: export(semester.get())  # Create a lambda function
    save_button = ttk.Button(save_window, text="Export all to CSV", command=export_command).grid(column=0, row=2)
    save_window.bind("<Return>", lambda event: export_command())  # Call the lambda function

# Create the main window
window = Tk()
window.title("GPA Calculator")
window.geometry("+500+200")


mainframe = ttk.Frame(window, padding="3 3 5 5") #, padding="3 3 5 5"
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))


# Style configs
style = ttk.Style()
style.configure("Custom.TLabel", padding=(5, 10))

style = ttk.Style()
style.configure("LeftPadded.TLabel", padding=5)

# Create welcome message at top of window
label = ttk.Label(mainframe, text="Welcome to GPA calculator!", style="Custom.TLabel")
label.grid(column=0, row=0, sticky=N, columnspan = 6)

# Storing grades and class names
gpa_dict = {}
all_gpa_points = []
all_credits = []
all_desigs = []

# Create section to input grades for this semester
ttk.Label(mainframe, text="Input grades for a semester", style="LeftPadded.TLabel").grid(column=0, row=1, sticky=W)

ttk.Label(mainframe, text="Class name", style="LeftPadded.TLabel").grid(column=0, row=2, sticky=W)
ttk.Label(mainframe, text="Grade").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Credits").grid(column=2, row=2, sticky=W)

class_name = StringVar()
class_entry = ttk.Entry(mainframe, textvariable=class_name) #, width=20
class_entry.grid(column=0, row=3, sticky=W, columnspan=4)
class_entry.focus()

grade = StringVar()
grade_entry = ttk.Entry(mainframe, textvariable=grade, width=5) #, width=5
grade_entry.grid(column=1, row=3, sticky=W)

credit = StringVar()
credit_entry = ttk.Entry(mainframe, width=5,textvariable=credit)  #width=5,
credit_entry.grid(column=2, row=3, columnspan=2, sticky=W)

# Create section to input grades for this semester
ttk.Label(mainframe, text="Designation:", style="LeftPadded.TLabel").grid(column=0, row=4, sticky=W)

H_check = StringVar(value="")
H_designation = ttk.Checkbutton(mainframe, text="H", variable=H_check)
H_designation.grid(column=0, row=5, sticky=W)


S_check = StringVar(value="")
S_designation = ttk.Checkbutton(mainframe, text="S", variable=S_check)
S_designation.grid(column=0, row=6, sticky=W)

N_check = StringVar(value="")
N_designation = ttk.Checkbutton(mainframe, text="N", variable=N_check)
N_designation.grid(column=0, row=5, sticky=(N,S))

Q_check = StringVar(value="")
Q_designation = ttk.Checkbutton(mainframe, text="Q", variable=Q_check)
Q_designation.grid(column=0, row=6, sticky=(N,S))

E_check = StringVar(value="")
E_designation = ttk.Checkbutton(mainframe, text="E", variable=E_check)
E_designation.grid(column=0, row=5, sticky=E)

W_check = StringVar(value="")
W_designation = ttk.Checkbutton(mainframe, text="W", variable=W_check)
W_designation.grid(column=0, row=6, sticky=E)


ttk.Button(mainframe, text="Add", command=add, width=3).grid(column=2, row=11, sticky=W)
window.bind("<Return>", add)

# Create semester message
ttk.Label(mainframe, text="Your grades for chosen semester", style="LeftPadded.TLabel").grid(column=0, row=12, sticky=W)

# Create the table
treeview = ttk.Treeview(mainframe, columns=('Class Name', 'Desig.', 'Grade', 'GPA Points'), show='headings')
treeview.column('Grade', width=40) 
treeview.heading('Grade', text='Grade')
treeview.column('Class Name', width=150) 
treeview.heading('Class Name', text='Class Name')
treeview.column('GPA Points', width=70)
treeview.heading('GPA Points', text='GPA Points')
treeview.column('Desig.', width=40)
treeview.heading('Desig.', text='Desig.')

treeview.grid(column=0, row=12, columnspan=6, sticky=(N, S, W, E))

# Find average GPA and letter grade
average_gpa = calculate_average_gpa()
average_grade = find_letter(average_gpa)

str_average_grade = StringVar()
str_average_gpa = StringVar()
str_average_grade.set(str(average_grade))
str_average_gpa.set(f"{average_gpa:.2f}")

ttk.Label(mainframe, text="Average Grade:", style="LeftPadded.TLabel").grid(column=0, row=13, sticky=W)
ttk.Label(mainframe, textvariable=str_average_grade).grid(column=0, row=13, sticky=(N,S,E))
ttk.Label(mainframe, text="Average GPA:", style="LeftPadded.TLabel").grid(column=1, row=13, sticky=E)
ttk.Label(mainframe, textvariable=str_average_gpa).grid(column=2, row=13, sticky=W)

#Save semester button (export data to csv file)
ttk.Button(mainframe, text="Save", command=save, width=7).grid(column=2, row=14, sticky=W)

window.mainloop()
