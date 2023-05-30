#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed May 24 20:57:05 2023

This script is a GPA calculator application built using the tkinter library 
in Python. It provides a graphical user interface (GUI) for users to input 
their class names, class numbers, grades and credits and calculates the GPA 
based on the entered data. It also provides the option to export the data 
to a CSV file.

@author: michellesandag
"""

from tkinter import *
from tkinter import ttk
import csv
from functools import partial



def add(entry_data, check_list, data_retrieval, treeview, 
        str_average_gpa, str_average_grade):
    """
    Defines the add command (allows user to add data for a class)

    Parameters
    ----------
    entry_data : list
        Contains class name, number, grade, and credit as entered by user.
    check_list : list
        Contains all designation checks (HSNEQW).
    data_retrieval : list
        Contains list of all credits, gpa points, designations, class numbers,
        and dictionary of class name and grade.
    treeview : tkinter widget
        The table in row 9 that displays class name, class number, and gpa
        points.
    str_average_gpa : string
        Average gpa of all entered classes.
    str_average_grade : string
        Letter grade corresponding to average gpa.

    Returns
    -------
    None.

    """
    
    # Retrieves user-entered data for Class name, Grade, Credits, GPA, Desig.
    class_name_val = entry_data[0].get()
    class_num_val = entry_data[1].get()
    grade_val = entry_data[2].get()
    credit_val = entry_data[3].get()
    
    # Correct values of pressed and unpressed checkbuttons
    update_checks(check_list)
    
    # Collect these designation strings in a variable
    desig_val = ""
    for item in check_list:
        desig_val += item.get()
    
    # Save retrieved data in lists or dictionaries
    data_retrieval[0].append(float(credit_val))
    gpa_points = float(find_gpa(grade_val)) * float(credit_val)
    data_retrieval[1].append(gpa_points)
    data_retrieval[2].append(desig_val)
    data_retrieval[3].append(class_num_val)
    data_retrieval[4][class_name_val] = grade_val
    
    if class_name_val and grade_val:
        # Add class data entry into the treeview table in row 9
        treeview.insert('', 'end', values=(class_name_val, class_num_val, 
                                           f"{gpa_points:.2f}"))
        # Reset variables
        entry_data[0].set("")
        entry_data[1].set('')
        entry_data[2].set('')
        entry_data[3].set('')
        disable_checks(check_list)
        
        # Recalculate average GPA and letter grade
        average_gpa = calculate_average_gpa(data_retrieval[0], 
                                            data_retrieval[1])
        average_grade = find_letter(average_gpa)
        
        # Update the average GPA and letter grade labels
        str_average_gpa.set(f"{average_gpa:.2f}")
        str_average_grade.set(average_grade)

def calculate_average_gpa(all_credits, all_gpa_points):
    """
    Calculates average GPA

    Parameters
    ----------
    all_credits : list
        Contains all credits entered by the user as floats.
    all_gpa_points : list
        Contains gpa points for each class entered by the user as floats.

    Returns
    -------
    float
        Returns the mean GPA (if user hasn't entered any classes, returns 0).

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
        Letter grade to the find the GPA for.

    Returns
    -------
    string
        Returns the GPA value corresponding to the entered letter_grade.

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
        GPA to find the letter grade for.

    Returns
    -------
    key : string
        Returns the letter grade corresponding to the gpa parameter.

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
            
def export(semester_number, username, data_retrieval, str_average_gpa, 
           str_average_grade, save_window, window):
    """
    Exports all data to a CSV file

    Parameters
    ----------
    semester_number : int
        The semester all the entered data corresponds to.
    data_retrieval : list
        Contains list of all credits, gpa points, designations, class numbers,
        and dictionary of class name and grade.
    str_average_gpa : string
        Average gpa of all entered classes.
    str_average_grade : string
        Letter grade corresponding to average gpa.

    Returns
    -------
    None.

    """


    # Exports in a file named semester_#.csv
    semesterfile = f"{username}_semester_{semester_number}.csv"
    with open(semesterfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        all_data = []
        counter = 0
        # Saves each individual data entry as a row in all_data list
        for class_name, grade in data_retrieval[4].items():
            all_data.append([class_name, data_retrieval[3][counter], 
                             f"{data_retrieval[1][counter]:.2f}", 
                            data_retrieval[0][counter], 
                            data_retrieval[2][counter]])
            counter += 1

        # Write the data to the CSV file
        writer.writerow(['Class Name', 'Number', 'GPA Points', 
                         'Credits', 'Designation'])
        writer.writerows(all_data)
        writer.writerow(['Average Grade', str_average_grade.get(),
                         'Average GPA', str_average_gpa.get(), '-'])
    csvfile.close()
    save_window.destroy()
    
    

def save(window, data_retrieval, str_average_gpa, str_average_grade):
    """
    Prompts user to specify which semester the previously entered data
    corresponds to

    Parameters
    ----------
    window : tkinter toplevel window
        Main window of the application.
    data_retrieval : list
        Contains list of all credits, gpa points, designations, class numbers,
        and dictionary of class name and grade.
    str_average_gpa : string
        Average gpa of all entered classes.
    str_average_grade : string
        Letter grade corresponding to average gpa.

    Returns
    -------
    None.

    """

    
    # Open a new window
    save_window = Toplevel(window)
    save_window.geometry("300x170+570+300")
    save_window.title("Semester Data Entry")
    saveframe = ttk.Frame(save_window, padding="5 5 7 7")
    saveframe.grid(column=0, row=0, sticky=(N, W, E, S))

    # Ask user to input username and semester number
    save_label = ttk.Label(saveframe, 
                           text="Please enter username and which semester\n" + 
                           "the previously entered data corresponds to",
                           style="Custom.TLabel")
    save_label.grid(column=0, row=0, sticky=N, columnspan=2)
    user_label = ttk.Label(save_window, text="Username", 
                               style="LeftPadded.TLabel")
    
    user_label.grid(column=0, row=1, sticky=W)
    
    semester_label = ttk.Label(save_window, text="Semester #", 
                               style="LeftPadded.TLabel")
    semester_label.grid(column=0, row=2, sticky=W)
    # Save username and semester number in a variable
    username = StringVar()
    user_entry = ttk.Entry(save_window, width=10, textvariable=username)
    user_entry.grid(column=0, row=1, sticky=E)
    user_entry.focus()
    
    semester = StringVar()
    semester_entry = ttk.Entry(save_window, width=10, textvariable=semester)
    semester_entry.grid(column=0, row=2, sticky=E)
    
    # Define a command for calling export function and apply to save button
    export_command = lambda: export(semester.get(), username.get(), 
                                    data_retrieval, str_average_gpa, 
                                    str_average_grade, save_window, window) 
    save_button = ttk.Button(save_window, text="Export all to CSV", 
                             command=export_command).grid(column=0, row=3)
    # Bind return key to export function
    save_window.bind("<Return>", lambda event: export_command())
    
def update_checks(all_checks):
    """
    Set pressed checks to labelled string and sets unpressed checks to 
    empty strings

    Parameters
    ----------
    all_checks : list
        Contains all designation checks (HSNEQW).

    Returns
    -------
    None.

    """

    checks = [(0, "H"), (1, "S"), (2, "N"), (3, "Q"),
              (4, "E"), (5, "W")]
    # Iterate over the checkbuttons and set pressed checks to the matching
    # values above and set unpressed checks to empty strings
    for check, label in checks:
        if all_checks[check].get() == "1":
            all_checks[check].set(label)
        else:
            all_checks[check].set("")
def disable_checks(all_checks):
    """
    Set all checks to their unpressed values

    Parameters
    ----------
    all_checks : list
        Contains all designation checks (HSNEQW).

    Returns
    -------
    None.

    """
    
    checks = [(0, "H"), (1, "S"), (2, "N"), (3, "Q"),
              (4, "E"), (5, "W")]
    for check, label in checks:
        all_checks[check].set(label)

def main():
    
    # Storing grades and class names
    all_credits = []
    all_gpa_points = []
    all_desigs = []
    all_num = []
    gpa_dict = {}
    
    # Create the main window and frame
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
    label = ttk.Label(mainframe, text="Welcome to GPA calculator!", 
                      style="Custom.TLabel")
    label.grid(column=0, row=0, sticky=N, columnspan = 6)
    
    
    # Create section to input grades for this semester
    ttk.Label(mainframe, text="Input grades for a semester",
              style="LeftPadded.TLabel").grid(column=0, row=1, sticky=W)
    
    ttk.Label(mainframe, text="Class name", 
              style="LeftPadded.TLabel").grid(column=0, row=2, sticky=W)
    ttk.Label(mainframe, text="Number").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text="Grade").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="Credits").grid(column=2, row=2, sticky=W)
    
    # Class name entry
    class_name = StringVar()
    class_entry = ttk.Entry(mainframe, textvariable=class_name , width=25)
    class_entry.grid(column=0, row=3, sticky=W, columnspan=4)
    class_entry.focus()
    
    # Class number entry
    class_num = StringVar()
    num_entry = ttk.Entry(mainframe, width=10,textvariable=class_num)
    num_entry.grid(column=1, row=3, sticky=W)
    
    # Grade entry
    grade = StringVar()
    grade_entry = ttk.Entry(mainframe, textvariable=grade, width=3)
    grade_entry.grid(column=1, row=3, sticky=E)
    
    # Credits entry
    credit = StringVar()
    credit_entry = ttk.Entry(mainframe, width=5,textvariable=credit) 
    credit_entry.grid(column=2, row=3, sticky=W)
    
    
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
    
    entry_data = [class_name, class_num, grade, credit]
    check_list = [H_check, S_check, N_check, Q_check, E_check, W_check]
    data_retrieval = [all_credits, all_gpa_points, 
                      all_desigs, all_num, gpa_dict]
    add_command = lambda: add(entry_data, check_list, data_retrieval, 
                              treeview, str_average_gpa, str_average_grade) 
    
    add_button= ttk.Button(mainframe, text="Add", 
                           command=add_command, width=3)
    add_button.grid(column=2, row=7, sticky=W)
    window.bind("<Return>", lambda event: add_command())
    
    # Create semester message
    ttk.Label(mainframe, text="Your grades for chosen semester", 
              style="LeftPadded.TLabel").grid(column=0, row=8, sticky=W)
    
    # Create the table
    treeview = ttk.Treeview(mainframe, 
                            columns=('Class Name', 'Number', 'GPA Points'), 
                            show='headings')
    treeview.column('Class Name', width=150) 
    treeview.heading('Class Name', text='Class Name')
    treeview.column('GPA Points', width=70)
    treeview.heading('GPA Points', text='GPA Points')
    treeview.column('Number', width=40)
    treeview.heading('Number', text='Number')
    
    treeview.grid(column=0, row=9, columnspan=6, sticky=(N, S, W, E))
    
    # Find average GPA and letter grade
    average_gpa = calculate_average_gpa(all_credits, all_gpa_points)
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
    save_command = lambda: save(window, data_retrieval, 
                                str_average_gpa, str_average_grade)  
    ttk.Button(mainframe, text="Save", 
               command=save_command, width=7).grid(column=2, row=11, sticky=W)
    
    window.mainloop()

if __name__ == "__main__": 
    main()