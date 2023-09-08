import tkinter as tk
from tkinter import filedialog
import csv

csv_file = None  

def open_file():
    global csv_file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        csv_file = file_path
        status_label.config(text=f"File opened: {csv_file}")

def remove_data():
    def delete_row():
        order_id = id_entry.get()
        data = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != order_id:
                    data.append(row)
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        remove_window.destroy()

    remove_window = tk.Toplevel(gui)
    remove_window.title("Remove Data")

    id_label = tk.Label(remove_window, text="Order ID:")
    id_label.pack()
    id_entry = tk.Entry(remove_window)
    id_entry.pack()
    delete_button = tk.Button(remove_window, text="Delete", command=delete_row)
    delete_button.pack()

def add_data():
    def save_data():
        data = [entry.get() for entry in data_entry]
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        add_window.destroy()

    add_window = tk.Toplevel(gui)
    add_window.title("Add Data")

    header_data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header_data = next(reader)

    data_entry = []

    for i, header_fields in enumerate(header_data):
        id_label = tk.Label(add_window, text=header_fields)
        id_label.grid(row=i, column=0, padx=10, pady=5)
        id_entry = tk.Entry(add_window)
        id_entry.grid(row=i, column=1, padx=10, pady=5)
        data_entry.append(id_entry)

    save_button = tk.Button(add_window, text="Save", command=save_data)
    save_button.grid(row=len(header_data), columnspan=2, padx=10, pady=10)

def query_data():
    def results():
        id = entry.get()
        result = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == id:
                    result.append(row)
        result_window = tk.Toplevel(gui)
        result_window.title("Query Result")
        for row in result:
            tk.Label(result_window, text=", ".join(row)).pack()

    query_window = tk.Toplevel(gui)
    query_window.title("Query Data")

    id_label = tk.Label(query_window, text="Order ID:")
    id_label.pack()
    entry = tk.Entry(query_window)
    entry.pack()
    query_button = tk.Button(query_window, text="Query", command=results)
    query_button.pack()

def edit_data():
    def edit():
        id = entry.get()
        update = [data_entry.get() for data_entry in fields]
        data = []
        
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == id:
                    row = update
                data.append(row)
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        edit_window.destroy()

    edit_window = tk.Toplevel(gui)
    edit_window.title("Edit Data")

    id_label = tk.Label(edit_window, text="Enter ID:")
    id_label.pack()
    entry = tk.Entry(edit_window)
    entry.pack()

    header_data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header_data = next(reader)

    fields = []

    for i, header_rows in enumerate(header_data):
        id_label = tk.Label(edit_window, text=header_rows)
        id_label.pack()
        id_entry = tk.Entry(edit_window)
        id_entry.pack()
        fields.append(id_entry)

    edit_button = tk.Button(edit_window, text="Edit", command=edit)
    edit_button.pack()

gui = tk.Tk()
gui.title("demo")

import_button = tk.Button(gui, text="Import", command=open_file)
remove_button = tk.Button(gui, text="Remove", command=remove_data)
add_button = tk.Button(gui, text="Add", command=add_data)
query_button = tk.Button(gui, text="Query", command=query_data)
edit_button = tk.Button(gui, text="Edit", command=edit_data)
status_label = tk.Label(gui, text="No file opened")


import_button.pack()
remove_button.pack()
add_button.pack()
query_button.pack()
edit_button.pack()
status_label.pack()

gui.mainloop()