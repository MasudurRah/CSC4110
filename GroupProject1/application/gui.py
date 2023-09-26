"""Modules to import tkinter, csv, and re functionality"""
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import re
import os

CSV_FILE = None

#regex validation
INVALID_CHARACTERS = r'[!#$%^&*()\_=+{}\[\]\\|?]'
EMAIL_PATTERN = r'\S+@\S+'
SSN_PATTERN = r'^\d{9}$'
COMPILE_INVALID = re.compile(INVALID_CHARACTERS)

def open_file():
    """Allows user to browse for csv file"""
    global CSV_FILE
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        CSV_FILE = file_path
        file_name = os.path.basename(CSV_FILE)  # Get just the file name without the path
        import_text.config(text=f"File opened: {file_name}")

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
    delete_screen.geometry("300x100")

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

        # Validation for special characters
        for value in data:
            if value and COMPILE_INVALID.search(value):
                messagebox.showerror("Error", "Special characters not allowed")
                return

        # Get the header data from the CSV file
        with open(CSV_FILE, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            header_data = next(reader)

        for i, header in enumerate(header_data):
            # Check if the header contains specific keywords and perform corresponding validations
            if "phone" in header.lower():
                if data[i] and len(data[i]) != 10:
                    messagebox.showerror("Error", "Phone number length is invalid")
                    return
            elif "email" in header.lower():
                if data[i] and not re.match(EMAIL_PATTERN, data[i]):
                    messagebox.showerror("Error", "Email is invalid")
                    return
            elif "ssn" in header.lower() or "social security" in header.lower():
                if data[i] and not re.match(SSN_PATTERN, data[i]):
                    messagebox.showerror("Error", "SSN length is invalid")
                    return

        # If all validations pass, save the data to the CSV file
        with open(CSV_FILE, 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        add_screen.destroy()

    # Created add window
    add_screen = tk.Toplevel(gui)
    add_screen.title("Add Data")

    header_data = []
    with open(CSV_FILE, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        header_data = next(reader)

    data_entry = []

    # Dynamic input box
    for i, header_fields in enumerate(header_data):
        id_text = tk.Label(add_screen, text=header_fields)
        id_text.grid(row=i, column=0, padx=10, pady=5)
        id_data = tk.Entry(add_screen)
        id_data.grid(row=i, column=1, padx=10, pady=5)
        data_entry.append(id_data)

    # Save button
    save_button = tk.Button(add_screen, text="Save", command=save)
    save_button.grid(row=len(header_data), columnspan=2, padx=10, pady=10)

@validate
def query_data():
    """Query data from imported csv file"""
    def perform_query():
        col_name = selected_column.get()
        query_value = id_data.get()
        result = []

        with open(CSV_FILE, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            col_names = next(reader)

            if col_name not in col_names:
                messagebox.showinfo("Result", f"Column '{col_name}' not found in the CSV file.")
                return

            for row in reader:
                # Change uppercase letters to lower
                row_value = row[col_names.index(col_name)].lower()
                if row_value == query_value:
                    result.append(row)

        if not result:
            messagebox.showinfo("Result", "No matching records found or "
                                  "input was not all lowercase")
        else:
            result_screen = tk.Toplevel(gui)
            result_screen.title("Query Result")

            # Create a canvas to hold the result frame with a horizontal scrollbar
            canvas = tk.Canvas(result_screen)
            canvas.pack(fill=tk.BOTH, expand=True)

            # Add a horizontal scrollbar
            scrollbar = tk.Scrollbar(result_screen, orient=tk.HORIZONTAL, command=canvas.xview)
            scrollbar.pack(fill=tk.X)

            # Configure the canvas to work with the scrollbar
            canvas.configure(xscrollcommand=scrollbar.set)

            # Create the result frame inside the canvas
            result_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=result_frame, anchor=tk.NW)

            # Function to update the canvas scrolling region
            def update_canvas_scroll_region(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            # Bind the canvas to update scrolling
            result_frame.bind("<Configure>", update_canvas_scroll_region)

            for i, col_name in enumerate(col_names):
                padded_col_name = col_name.ljust(20)
                columntext = tk.Label(result_frame, text=padded_col_name)
                columntext.grid(row=i, column=0)

                for j, row in enumerate(result):
                    row_data = row[i].ljust(20)

                    if "ssn" in col_name.lower() or "social security" in col_name.lower():
                        ssn = f"{row_data[:3]}-{row_data[3:5]}-{row_data[5:]}"
                        tk.Label(result_frame, text=ssn).grid(row=i, column=j + 1)
                    elif "phone" in col_name.lower():
                        phone = f"{row_data[:3]}-{row_data[3:6]}-{row_data[6:]}"
                        tk.Label(result_frame, text=phone).grid(row=i, column=j + 1)
                    else:
                        tk.Label(result_frame, text=row_data).grid(row=i, column=j + 1)

    # Create new query window
    query_screen = tk.Toplevel(gui)
    query_screen.title("Query Data")
    query_screen.geometry("300x500")

    # Radio buttons for column selection
    selected_column = tk.StringVar()
    selected_column.set("")  # Initialize to an empty value

    col_label = tk.Label(query_screen, text="Select Column to Search By:")
    col_label.pack(pady=20)

    col_names = []  # Initialize with column names from your CSV file header
    with open(CSV_FILE, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        col_names = next(reader)

    for col_name in col_names:
        col_radio = tk.Radiobutton(query_screen, text=col_name,
                                    variable=selected_column, value=col_name)
        col_radio.pack()

    # Input box for query
    id_text = tk.Label(query_screen, text="Enter Value to Search:")
    id_text.pack()
    id_data = tk.Entry(query_screen)
    id_data.pack()

    # Query button
    query_button = tk.Button(query_screen, text="Query", command=perform_query)
    query_button.pack()

@validate
def edit_data():
    """Edit data from imported csv file"""
    def edit():
        id_value = id_data.get()
        update = [data_entry.get() for data_entry in fields]

        # Validation for special characters
        for value in update:
            if COMPILE_INVALID.search(value):
                messagebox.showerror("Error", "Special characters not allowed")
                return

        # Validation for specific columns
        for header, value in zip(header_data, update):
            if "phone" in header.lower():
                # Check if the value has exactly 10 digits if it's not empty
                if value and (not value.isdigit() or len(value) != 10):
                    messagebox.showerror("Error", "Phone number length is invalid")
                    return
            elif "email" in header.lower():
                # Check if the value contains '@' if it's not empty
                if value and ('@' not in value):
                    messagebox.showerror("Error", "Email is invalid")
                    return
            elif "ssn" in header.lower() or "social security" in header.lower():
                # Check if the value has exactly 9 digits if it's not empty
                if value and (not value.isdigit() or len(value) != 9):
                    messagebox.showerror("Error", "SSN length is invalid")
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

    # Creates a new edit window
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

    # Creates dynamic edit input boxes
    for header_row in header_data:
        id_text = tk.Label(edit_screen, text=header_row)
        id_text.pack()
        id_entry = tk.Entry(edit_screen)
        id_entry.pack()
        fields.append(id_entry)

    # Edit button
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
