#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:40:13 2023

Main application: connected to GPA_calculator and req_tracker

@author: michellesandag
"""

import tkinter as tk
from tkinter.constants import N,W,E,S
from tkinter import ttk
import os #for working with directory paths
import re #for matching regexes
import subprocess #for running other python scripts

def create_widgets(mainframe):
    
    # Create welcome message at top of window
    label = tk.Label(mainframe, text="Welcome to cumulative GPA and requirement tracker!", 
                       bg="lightblue", padx="15", pady="15") #, fg="white")
    label.grid(column=0, row=0, sticky=N, columnspan = 6)
    
    # Ask user for username
    user_label = tk.Label(mainframe, text="Enter username:", 
                       bg="lightblue", padx="15") #, fg="white")
    user_label.grid(column=0, row=1, sticky=W)
    
    username = tk.StringVar()
    user_entry = ttk.Entry(mainframe, textvariable=username, width=15)
    user_entry.grid(column=1, row=1, sticky=W, padx=(15,15))
    
    # Retrieve data button
    retrieve_command = lambda: retrieve_data(username.get(), mainframe, 
                                             user_entry, retrieve_button)
    retrieve_button = tk.Button(mainframe, text="Retrieve data", 
                                bg="lightblue", width=10,
                                highlightbackground="lightblue",
                                 command=retrieve_command)
    retrieve_button.grid(column=1, row=2, sticky=E, padx=(15,15))
    
def retrieve_data(name, frame, entry, button):
    entry.config(state=tk.DISABLED)
    button.config(state=tk.DISABLED)
    
    match_num = 0
    folder_path = os.getcwd()
    regex_pattern = rf"{name}_semester_\d+\.csv"
    
    tk.Label(frame, text=f"GPA data found for {name} in files:", 
                       bg="lightblue", padx="15").grid(column=0, row=3, sticky=W)
    
    for filename in os.listdir(folder_path):
        if re.search(regex_pattern, filename):
            match_label = tk.Label(frame, text=filename, bg="lightblue", 
                                   padx="25") #, fg="white")
            match_label.grid(column=0, row=4 + match_num, sticky=W)
            match_num += 1
            
    if match_num == 0:
        unmatch_label = tk.Label(frame, text="Not found", 
                                 bg="lightblue", padx="25")
        unmatch_label.grid(column=0, row=4, sticky=W)
    else:
        continue_button = tk.Button(frame, text="Continue", 
                                    bg="lightblue", width=10,
                                    highlightbackground="lightblue",
                                     command=continue_command)
        continue_button.grid(column=1, row=5+match_num, sticky=E, padx=(15,15),
                             pady = (0, 15))
    add_button = tk.Button(frame, text="Add GPA data", 
                                bg="lightblue", width=10,
                                highlightbackground="lightblue",
                                 command=add_command)
    add_button.grid(column=0, row=5+match_num, sticky=W, padx=(15,15),
                    pady = (0,15))

def continue_command():
    # Run cumulative GPA calculator
    subprocess.run(["python", f"{os.getcwd()}/cumulative_gpa.py"])
    
def add_command():
    # Run semesterly GPA calculator
    subprocess.run(["python", f"{os.getcwd()}/semesterly_gpa.py"])

def main():
    # Create the main window and frame
    window = tk.Tk()
    window.title("Student Information")
    window.geometry("+500+200")
    window.configure(background="lightblue")

    mainframe = tk.Frame(window, bg="lightblue") #, padding="3 3 5 5"
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    create_widgets(mainframe)
    
    window.mainloop()
    
if __name__ == "__main__": 
    main()