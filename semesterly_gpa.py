#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 20:57:05 2023

My preliminary GPA calculator code

@author: michellesandag
"""

from tkinter import *
from tkinter import ttk

# Defining the add command (user adds their grade for a class)
def add(*args):
    class_name_val = class_name.get()
    grade_val = grade.get()
    credit_val = credit.get()
    all_credits.append(float(credit_val))
    gpa_points = float(find_gpa(grade_val)) * float(credit_val)
    all_gpa_points.append(gpa_points)
    gpa_val = find_gpa(grade_val)
    if class_name_val and grade_val:
        gpa_dict[class_name_val] = float(gpa_val)
        treeview.insert('', 'end', values=(class_name_val, grade_val, gpa_points))
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
            break  # Exit the loop after finding the first match

# Defining the finish command (exporting user's grades, classes, etc.)
def finish(*args):
    pass


# Create the main window
window = Tk()
window.title("GPA Calculator")

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

# Create section to input grades for this semester
semester = StringVar()
semester.set("1")
ttk.Label(mainframe, text="Input grades for semester #", style="LeftPadded.TLabel").grid(column=0, row=1, sticky=W)
ttk.Label(mainframe, textvariable=semester).grid(column=1, row=1)

ttk.Label(mainframe, text="Class name", style="LeftPadded.TLabel").grid(column=0, row=2, columnspan=2)
ttk.Label(mainframe, text="Grade").grid(column=2, row=2)
ttk.Label(mainframe, text="Credits").grid(column=3, row=2, sticky=W)

class_name = StringVar()
class_entry = ttk.Entry(mainframe, width=20, textvariable=class_name)
class_entry.grid(column=0, row=3, sticky=W, columnspan=4)

grade = StringVar()
grade_entry = ttk.Entry(mainframe, width=5, textvariable=grade)
grade_entry.grid(column=2, row=3)

credit = StringVar()
credit_entry = ttk.Entry(mainframe, width=5, textvariable=credit)
credit_entry.grid(column=3, row=3, columnspan=2, sticky=W)

ttk.Button(mainframe, text="Add", command=add, width=3).grid(column=3, row=4, sticky=W)
window.bind("<Return>", add)

# Create semester message
ttk.Label(mainframe, text="Your grades for semester #", style="LeftPadded.TLabel").grid(column=0, row=5, sticky=W)
ttk.Label(mainframe, textvariable=semester).grid(column=1, row=5)

# Create the table
treeview = ttk.Treeview(mainframe, columns=('Class Name', 'Grade', 'GPA Points'), show='headings')
treeview.column('Grade', width=70) 
treeview.heading('Class Name', text='Class Name')
treeview.column('Class Name', width=150) 
treeview.heading('Grade', text='Grade')
treeview.column('GPA Points', width=70)
treeview.heading('GPA Points', text='GPA Points')

treeview.grid(column=0, row=6, columnspan=6, sticky=(N, S, W, E))

# Find average GPA and letter grade
average_gpa = calculate_average_gpa()
average_grade = find_letter(average_gpa)

str_average_grade = StringVar()
str_average_gpa = StringVar()
str_average_grade.set(str(average_grade))
str_average_gpa.set(f"{average_gpa:.2f}")

ttk.Label(mainframe, text="Average Grade:", style="LeftPadded.TLabel").grid(column=0, row=7, sticky=W)
ttk.Label(mainframe, textvariable=str_average_grade).grid(column=0, row=7, sticky=E)
ttk.Label(mainframe, text="Average GPA:", style="LeftPadded.TLabel").grid(column=2, row=7, sticky=E)
ttk.Label(mainframe, textvariable=str_average_gpa).grid(column=3, row=7, sticky=W)

#Save semester button (export data to csv file)
ttk.Button(mainframe, text="Save", command=finish, width=7).grid(column=3, row=8, sticky=W)

window.mainloop()
