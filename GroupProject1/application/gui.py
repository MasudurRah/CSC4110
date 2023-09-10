import tkinter as tk
from tkinter import filedialog
import csv

csv_file = None  

def open_file():
    global csv_file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        csv_file = file_path
        import_text.config(text=f"File opened: {csv_file}")

def remove_data():
    def delete():
        row_id = id_data.get()
        data = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != row_id:
                    data.append(row)
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        delete_screen.destroy()

    delete_screen = tk.Toplevel(gui)
    delete_screen.title("Remove Data")

    id_text = tk.Label(delete_screen, text="Enter ID:")
    id_text.pack()
    id_data = tk.Entry(delete_screen)
    id_data.pack()
    delete_button = tk.Button(delete_screen, text="Delete", command=delete)
    delete_button.pack()

def add_data():
    def save():
        data = [entry.get() for entry in data_entry]
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        add_screen.destroy()

    add_screen = tk.Toplevel(gui)
    add_screen.title("Add Data")

    header_data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header_data = next(reader)

    data_entry = []

    for i, header_fields in enumerate(header_data):
        id_text = tk.Label(add_screen, text=header_fields)
        id_text.grid(row=i, column=0, padx=10, pady=5)
        id_data = tk.Entry(add_screen)
        id_data.grid(row=i, column=1, padx=10, pady=5)
        data_entry.append(id_data)

    save_button = tk.Button(add_screen, text="Save", command=save)
    save_button.grid(row=len(header_data), columnspan=2, padx=10, pady=10)

def query_data():
    def results():
        row_data = id_data.get()
        result = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == row_data:
                    result.append(row)
        result_screen = tk.Toplevel(gui)
        result_screen.title("Query Result")
        for row in result:
            tk.Label(result_screen, text=", ".join(row)).pack()

    query_screen = tk.Toplevel(gui)
    query_screen.title("Query Data")

    id_text = tk.Label(query_screen, text="Enter ID:")
    id_text.pack()
    id_data = tk.Entry(query_screen)
    id_data.pack()
    query_button = tk.Button(query_screen, text="Query", command=results)
    query_button.pack()

def edit_data():
    def edit():
        id = id_data.get()
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
        edit_screen.destroy()

    edit_screen = tk.Toplevel(gui)
    edit_screen.title("Edit Data")

    id_text = tk.Label(edit_screen, text="Enter ID:")
    id_text.pack()
    id_data = tk.Entry(edit_screen)
    id_data.pack()

    header_data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header_data = next(reader)

    fields = []

    for i, header_rows in enumerate(header_data):
        id_text = tk.Label(edit_screen, text=header_rows)
        id_text.pack()
        id_entry = tk.Entry(edit_screen)
        id_entry.pack()
        fields.append(id_entry)

    edit_button = tk.Button(edit_screen, text="Edit", command=edit)
    edit_button.pack()

gui = tk.Tk()
gui.title("CSV Editor")
gui.geometry("800x400")

import_button = tk.Button(gui, text="Import", command=open_file)
remove_button = tk.Button(gui, text="Remove", command=remove_data)
add_button = tk.Button(gui, text="Add", command=add_data)
query_button = tk.Button(gui, text="Query", command=query_data)
edit_button = tk.Button(gui, text="Edit", command=edit_data)
import_text = tk.Label(gui, text="No file opened")


import_button.pack()
remove_button.pack()
add_button.pack()
query_button.pack()
edit_button.pack()
import_text.pack()

gui.mainloop()