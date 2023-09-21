"""Modules to import tkinter, csv, and re functionality"""
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import re

CSV_FILE = None

#regex validation
INVALID_CHARACTERS = r'[!#$%^&*()\_=+{}\[\]\\|?]'
compile_invalid = re.compile(INVALID_CHARACTERS)

def open_file():
    """Allows user to browse for csv file"""
    global CSV_FILE
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path: #Sets the csv file and prints location
        CSV_FILE = file_path
        import_text.config(text=f"File opened: {CSV_FILE}")

def validate(function):
    """Validates if csv file is imported"""
    def validate_button():
        if CSV_FILE is None: #Validation opens new warning
            messagebox.showwarning("Warning", "No CSV file found")
        else:
            function()
    return validate_button

@validate
def remove_data():
    """Removes data from imported csv file"""
    def delete():
        row_id = id_data.get()
        data = []
        with open(CSV_FILE, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != row_id:
                    data.append(row)
        with open(CSV_FILE, 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
        delete_screen.destroy()

    #Opens delete window
    delete_screen = tk.Toplevel(gui)
    delete_screen.title("Remove Data")

    #Delete window functionality
    id_text = tk.Label(delete_screen, text="Enter ID:")
    id_text.pack()
    id_data = tk.Entry(delete_screen)
    id_data.pack()
    delete_button = tk.Button(delete_screen, text="Delete", command=delete)
    delete_button.pack()

@validate
def add_data():
    """Add data to imported csv file"""
    def save():
        data = [entry.get() for entry in data_entry]

        if all(not entry for entry in data):
            messagebox.showerror("Error", "Input needed")
            return

        #Validation for special characters
        for value in data:
            if compile_invalid.search(value):
                messagebox.showerror("Error", "Special characters not allowed")
                return

        with open(CSV_FILE, 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        add_screen.destroy()

    #Created add window
    add_screen = tk.Toplevel(gui)
    add_screen.title("Add Data")

    header_data = []
    with open(CSV_FILE, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        header_data = next(reader)

    data_entry = []

    #Dynamic input box
    for i, header_fields in enumerate(header_data):
        id_text = tk.Label(add_screen, text=header_fields)
        id_text.grid(row=i, column=0, padx=10, pady=5)
        id_data = tk.Entry(add_screen)
        id_data.grid(row=i, column=1, padx=10, pady=5)
        data_entry.append(id_data)

    #Save button
    save_button = tk.Button(add_screen, text="Save", command=save)
    save_button.grid(row=len(header_data), columnspan=2, padx=10, pady=10)

@validate
def query_data():
    """Query data from imported csv file"""
    def results():
        row_data = id_data.get()
        result = []
        col_names = []
        with open(CSV_FILE, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            col_names = next(reader)
            for row in reader:
                if row[0] == row_data:
                    result.append(row)

        result_screen = tk.Toplevel(gui)
        result_screen.title("Query Result")

        #Validation for no matching record
        if not result:
            messagebox.showinfo("Result", "No matching records found")
        else:
            frame = tk.Frame(result_screen)
            frame.pack()

            for i, col_name in enumerate(col_names):
                padded_col_name = col_name.ljust(20)
                columntext = tk.Label(frame, text=padded_col_name)
                columntext.grid(row=i, column=0)

                for j, row in enumerate(result):
                    row_data = row[i].ljust(20)

                    #SSN and phone number data format
                    if "ssn" in col_name.lower() or "social security" in col_name.lower():
                        ssn = f"{row_data[:3]}-{row_data[3:5]}-{row_data[5:]}"
                        tk.Label(frame, text=ssn).grid(row=i, column=j + 1)
                    elif "phone" in col_name.lower():
                        phone = f"{row_data[:3]}-{row_data[3:6]}-{row_data[6:]}"
                        tk.Label(frame, text=phone).grid(row=i, column=j + 1)
                    else:
                        tk.Label(frame, text=row_data).grid(row=i, column=j + 1)

    #Create new query window
    query_screen = tk.Toplevel(gui)
    query_screen.title("Query Data")

    #Input box for query
    id_text = tk.Label(query_screen, text="Enter ID:")
    id_text.pack()
    id_data = tk.Entry(query_screen)
    id_data.pack()

    #Query button
    query_button = tk.Button(query_screen, text="Query", command=results)
    query_button.pack()

@validate
def edit_data():
    """Edit data from imported csv file"""
    def edit():
        id_value = id_data.get()
        update = [data_entry.get() for data_entry in fields]

        #Validation for special characters
        for value in update:
            if compile_invalid.search(value):
                messagebox.showerror("Error", "Special characters not allowed")
                return

        data = []

        with open(CSV_FILE, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == id_value:
                    row = update
                data.append(row)
        with open(CSV_FILE, 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
        edit_screen.destroy()

    #Creates new edit window
    edit_screen = tk.Toplevel(gui)
    edit_screen.title("Edit Data")

    id_text = tk.Label(edit_screen, text="Enter ID:")
    id_text.pack()
    id_data = tk.Entry(edit_screen)
    id_data.pack()

    header_data = []
    with open(CSV_FILE, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        header_data = next(reader)

    fields = []

    #Creates dynamic edit input box
    for header_rows in header_data:
        id_text = tk.Label(edit_screen, text=header_rows)
        id_text.pack()
        id_entry = tk.Entry(edit_screen)
        id_entry.pack()
        fields.append(id_entry)

    #Edit button
    edit_button = tk.Button(edit_screen, text="Edit", command=edit)
    edit_button.pack()



#Creates the gui name and size
gui = tk.Tk()
gui.title("CSV Editor")
gui.geometry("300x400")

#Adds header text
title_text = tk.Label(gui, text="CSV Editor", font=("Arial", 24))
title_text.pack(pady=20)

#Adds all of the buttons
import_button = tk.Button(gui, text="Import", command=open_file, height=3, width=25)
remove_button = tk.Button(gui, text="Remove", command=remove_data, height=3, width=25)
add_button = tk.Button(gui, text="Add", command=add_data, height=3, width=25)
query_but = tk.Button(gui, text="Query", command=query_data, height=3, width=25)
edit_but = tk.Button(gui, text="Edit", command=edit_data, height=3, width=25)
import_text = tk.Label(gui, text="No file opened", height=3, width=25)

import_button.pack()
remove_button.pack()
add_button.pack()
query_but.pack()
edit_but.pack()
import_text.pack()

gui.mainloop()
