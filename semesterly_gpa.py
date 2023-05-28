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

all_credits = []
all_gpa_points = []
all_desigs = []
gpa_dict = {}


def add():
    """
    Defines the add command (allows user to add data for a class)

    Returns
    -------
    None.

    """
    # Retrieves user-entered data for Class name, Grade, Credits, GPA, Desig.
    class_name_val = class_name.get()
    grade_val = grade.get()
    credit_val = credit.get()
    checks = [(H_check, "H"), (S_check, "S"), (N_check, "N"), (Q_check, "Q"),
              (E_check, "E"), (W_check, "W")]
    # Iterate over the checkbuttons and set pressed checks to the corresponding
    # values above and set unpressed checks to empty strings
    for check, label in checks:
        if check.get() == "1":
            check.set(label)
        else:
            check.set("")
    # Collect these designation strings in a variable
    desig_val = H_check.get() + S_check.get() + N_check.get() + Q_check.get()
    desig_val += E_check.get() + W_check.get()
    
    # Save retrieved data in lists or dictionaries
    all_credits.append(float(credit_val))
    gpa_points = float(find_gpa(grade_val)) * float(credit_val)
    all_gpa_points.append(gpa_points)
    all_desigs.append(desig_val)
    gpa_dict[class_name_val] = grade_val
    
    if class_name_val and grade_val:
        # Add class data entry into the treeview table in row 9
        treeview.insert('', 'end', values=(class_name_val, desig_val, 
                                grade_val, gpa_points))
        class_name.set("")
        grade.set('')
        credit.set('')
        
        # Recalculate average GPA and letter grade
        average_gpa = calculate_average_gpa()
        average_grade = find_letter(average_gpa)
        
        # Update the average GPA and letter grade labels
        str_average_gpa.set(f"{average_gpa:.2f}")
        str_average_grade.set(average_grade)

def calculate_average_gpa():
    """
    Calculates average GPA

    Returns
    -------
    float
        Returns the mean GPA (if user hasn't entered any classes, returns 0)

    """
    if sum(all_credits)== 0:
        return 0
    else:
        return sum(all_gpa_points)/sum(all_credits)
        
def find_gpa(letter_grade):
    """
    Finds GPA given a letter grade

    Parameters
    ----------
    letter_grade : string
        Letter grade to the find the GPA for

    Returns
    -------
    string
        Returns the GPA value corresponding to the entered letter_grade

    """
    gpa_letter = {
        "A+": 4.0, "A": 4.0, "A-": 3.7, 
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7
    }
    return str(gpa_letter[letter_grade])

def find_letter(gpa):
    """
    Finds letter grade given a GPA

    Parameters
    ----------
    gpa : float
        GPA to find the letter grade for

    Returns
    -------
    key : string
        Returns the letter grade corresponding to the gpa parameter

    """
    gpa_letter = {
        "A+": 4.0, "A": 4.0, "A-": 3.7, 
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7
    }
    
    # If gpa is equal to or greater than the value in the above dictionary,
    # the key is the corresponding letter grade
    for key, value in gpa_letter.items():
        if gpa >= value:
            return key
            
def export(semester_number):
    """
    Exports all data to a CSV file

    Parameters
    ----------
    semester_number : int
        The semester all the entered data corresponds to

    Returns
    -------
    None.

    """
    # Exports in a file named semester_#.csv
    semesterfile = f"semester_{semester_number}.csv"
    with open(semesterfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        all_data = []
        counter = 0
        # Saves each individual data entry as a row in all_data list
        for class_name, grade in gpa_dict.items():
            all_data.append([class_name, grade, all_gpa_points[counter], 
                            all_credits[counter], all_desigs[counter]])
            counter += 1

        # Write the data to the CSV file
        writer.writerow(['Class Name', 'Grade', 'GPA Points', 
                         'Credits', 'Designation'])
        writer.writerows(all_data)
        writer.writerow(['Average Grade', str_average_grade.get(),
                         'Average GPA', str_average_gpa.get(), '-'])

def save():
    """
    Prompts user to specify which semester the previously entered data
    corresponds to

    Returns
    -------
    None.

    """
    
    # Open a new window
    save_window = Toplevel(window)
    save_window.geometry("270x130+570+300")
    save_window.title("Semester Data Entry")
    saveframe = ttk.Frame(save_window, padding="5 5 7 7")
    saveframe.grid(column=0, row=0, sticky=(N, W, E, S))

    # Ask user to input semester number
    save_label = ttk.Label(saveframe, 
                           text="Please enter which semester the \n" + 
                           "previously entered data corresponds to",
                           style="Custom.TLabel")
    save_label.grid(column=0, row=0, sticky=N, columnspan=2)
    semester_label = ttk.Label(save_window, text="Semester #", 
                               style="LeftPadded.TLabel")
    semester_label.grid(column=0, row=1, sticky=W)
    
    semester = StringVar()
    semester_entry = ttk.Entry(save_window, width=10, textvariable=semester)
    semester_entry.grid(column=0, row=1, sticky=E)
    semester_entry.focus()
    
    # Define a command for calling export(semester) and apply to save button
    export_command = lambda: export(semester.get())  # Create a lambda function
    save_button = ttk.Button(save_window, text="Export all to CSV", 
                             command=export_command).grid(column=0, row=2)
    # Call the lambda function
    save_window.bind("<Return>", lambda event: export_command())

def main():
    
    global class_name, grade, credit, H_check, S_check, N_check, Q_check
    global E_check, W_check, treeview, str_average_gpa, str_average_grade
    global window
    
    # Create the main window and frame
    window = Tk()
    window.title("GPA Calculator")
    window.geometry("+500+200")
    ttk.Frame(window, padding="3 3 5 5") #, padding="3 3 5 5"
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    
    
    # Style configs
    style = ttk.Style()
    style.configure("Custom.TLabel", padding=(5, 10))
    
    style = ttk.Style()
    style.configure("LeftPadded.TLabel", padding=5)
    
    # Create welcome message at top of window
    label = ttk.Label(mainframe, text="Welcome to GPA calculator!", 
                      style="Custom.TLabel")
    label.grid(column=0, row=0, sticky=N, columnspan = 6)
    
    # Storing grades and class names
    gpa_dict = {}
    all_gpa_points = []
    all_credits = []
    all_desigs = []
    
    # Create section to input grades for this semester
    ttk.Label(mainframe, text="Input grades for a semester",
              style="LeftPadded.TLabel").grid(column=0, row=1, sticky=W)
    
    ttk.Label(mainframe, text="Class name", 
              style="LeftPadded.TLabel").grid(column=0, row=2, sticky=W)
    ttk.Label(mainframe, text="Grade").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text="Credits").grid(column=2, row=2, sticky=W)
    
    # Class name entry
    class_name = StringVar()
    class_entry = ttk.Entry(mainframe, textvariable=class_name)
    class_entry.grid(column=0, row=3, sticky=W, columnspan=4)
    class_entry.focus()
    
    # Grade entry
    grade = StringVar()
    grade_entry = ttk.Entry(mainframe, textvariable=grade, width=5)
    grade_entry.grid(column=1, row=3, sticky=W)
    
    # Credits entry
    credit = StringVar()
    credit_entry = ttk.Entry(mainframe, width=5,textvariable=credit) 
    credit_entry.grid(column=2, row=3, columnspan=2, sticky=W)
    
    # Create section to input grades for this semester
    ttk.Label(mainframe, text="Designation:", 
              style="LeftPadded.TLabel").grid(column=0, row=4, sticky=W)
    
    # Create checkbuttons for class designations
    # Humanities
    H_check = StringVar(value="")
    H_designation = ttk.Checkbutton(mainframe, text="H", variable=H_check)
    H_designation.grid(column=0, row=5, sticky=W)
    
    # Social & Behavioural Sciences
    S_check = StringVar(value="")
    S_designation = ttk.Checkbutton(mainframe, text="S", variable=S_check)
    S_designation.grid(column=0, row=6, sticky=W)
    
    # Natural Sciences
    N_check = StringVar(value="")
    N_designation = ttk.Checkbutton(mainframe, text="N", variable=N_check)
    N_designation.grid(column=0, row=5, sticky=(N,S))
    
    # Quantitative Studies
    Q_check = StringVar(value="")
    Q_designation = ttk.Checkbutton(mainframe, text="Q", variable=Q_check)
    Q_designation.grid(column=0, row=6, sticky=(N,S))
    
    # Engineering
    E_check = StringVar(value="")
    E_designation = ttk.Checkbutton(mainframe, text="E", variable=E_check)
    E_designation.grid(column=0, row=5, sticky=E)
    
    # Writing-Intensive
    W_check = StringVar(value="")
    W_designation = ttk.Checkbutton(mainframe, text="W", variable=W_check)
    W_designation.grid(column=0, row=6, sticky=E)
    
    # Button for adding entry to table
    ttk.Button(mainframe, text="Add", command=add,
               width=3).grid(column=2, row=7, sticky=W)
    window.bind("<Return>", add)
    
    # Create semester message
    ttk.Label(mainframe, text="Your grades for chosen semester", 
              style="LeftPadded.TLabel").grid(column=0, row=8, sticky=W)
    
    # Create the table
    treeview = ttk.Treeview(mainframe, 
                            columns=('Class Name', 'Desig.', 'Grade', 'GPA Points'), 
                            show='headings')
    treeview.column('Grade', width=40) 
    treeview.heading('Grade', text='Grade')
    treeview.column('Class Name', width=150) 
    treeview.heading('Class Name', text='Class Name')
    treeview.column('GPA Points', width=70)
    treeview.heading('GPA Points', text='GPA Points')
    treeview.column('Desig.', width=40)
    treeview.heading('Desig.', text='Desig.')
    
    treeview.grid(column=0, row=9, columnspan=6, sticky=(N, S, W, E))
    
    # Find average GPA and letter grade
    average_gpa = calculate_average_gpa()
    average_grade = find_letter(average_gpa)
    
    str_average_grade = StringVar()
    str_average_gpa = StringVar()
    str_average_grade.set(str(average_grade))
    str_average_gpa.set(f"{average_gpa:.2f}")
    
    ttk.Label(mainframe, text="Average Grade:", 
              style="LeftPadded.TLabel").grid(column=0, row=10, sticky=W)
    ttk.Label(mainframe, textvariable=str_average_grade).grid(
        column=0, row=10, sticky=(N,S,E))
    ttk.Label(mainframe, text="Average GPA:", 
              style="LeftPadded.TLabel").grid(column=1, row=10, sticky=E)
    ttk.Label(mainframe, 
              textvariable=str_average_gpa).grid(column=2, row=10, sticky=W)
    
    #Save semester button (export data to csv file)
    ttk.Button(mainframe, text="Save", 
               command=save, width=7).grid(column=2, row=11, sticky=W)
    
    window.mainloop()

if __name__ == "__main__": 
    main()