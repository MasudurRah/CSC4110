import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random
import json
import re

IMAGE_PATH = "GroupProject3/files/redlogo.png"

def check_credentials(username, password):
    with open("GroupProject3/files/user_credentials.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row and len(row) >= 2 and row[0] == username and row[1] == password:
                return True
    return False

def generate_unique_ticket_number(existing_ticket_numbers):
    while True:
        new_ticket_number = str(random.randint(10000, 99999))
        if new_ticket_number not in existing_ticket_numbers:
            existing_ticket_numbers.add(new_ticket_number)
            return new_ticket_number

existing_ticket_numbers = set()
with open("GroupProject3/files/tickets.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        existing_ticket_numbers.add(row[0])

current_username = ""

def login():
    global current_username
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    if check_credentials(entered_username, entered_password):
        current_username = entered_username
        login_window.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Incorrect Login", "Invalid username or password")

def convert_to_json():
    json_filename = "GroupProject3/files/tickets.json"
    ticket_data = []

    with open("GroupProject3/files/tickets.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if row[5] == "True":
                ticket = {
                    "Ticket Number": row[0],
                    "Support Type": row[1],
                    "Name": row[2],
                    "Description": row[3],
                    "Reporter": row[4],
                    "Status": row[5]
                }
                ticket_data.append(ticket)

    with open(json_filename, 'w') as json_file:
        json.dump(ticket_data, json_file, indent=4)

    messagebox.showinfo("JSON Conversion", "Data has been converted to JSON")


def open_dashboard():
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")

    dashboard_window.geometry("1250x500")
    dashboard_window.configure(padx=20, pady=20)

    dashboard_logo_image = tk.PhotoImage(file="GroupProject3/files/redlogo.png").subsample(2, 2) 
    dashboard_logo_label = tk.Label(dashboard_window, image=dashboard_logo_image)
    dashboard_logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    def create_login_window():
        global login_window
        login_window = tk.Tk()
        login_window.title("Login")

        login_window.geometry("370x270")
        login_window.configure(padx=20, pady=20)

        logout_label = tk.Label(login_window, text="You have successfully logged out.")
        logout_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        global username_entry, password_entry

        username_label = tk.Label(login_window, text="Username:")
        username_entry = tk.Entry(login_window)
        password_label = tk.Label(login_window, text="Password:")
        password_entry = tk.Entry(login_window, show="*")

        login_button = tk.Button(login_window, text="Login", command=login)

        username_label.grid(row=1, column=0, padx=10, pady=10)
        username_entry.grid(row=1, column=1, padx=10, pady=10)
        password_label.grid(row=2, column=0, padx=10, pady=10)
        password_entry.grid(row=2, column=1, padx=10, pady=10)
        login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def logout():
        dashboard_window.destroy()
        create_login_window()

    def open_ticket_window(selected_row):
        ticket_window = tk.Toplevel(dashboard_window)
        ticket_window.title("Ticket Details")
        ticket_number = selected_row[0]
        support_type = selected_row[1]
        name = selected_row[2]
        description = selected_row[3]
        reporter = selected_row[4]
        status = selected_row[5]

        def toggle_ticket_status():
            nonlocal status
            if status == "True":
                status = "False"
            else:
                status = "True"

            with open("GroupProject3/files/tickets.csv", 'r', newline='') as file:
                rows = list(csv.reader(file))
                for row in rows:
                    if row[0] == ticket_number:
                        row[5] = status
                        break

            with open("GroupProject3/files/tickets.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            toggle_button.config(text="Close Ticket" if status == "False" else "Open Ticket")
            refresh_treeview()

        details_label = tk.Label(ticket_window, text=f"Ticket Number: {ticket_number}\nSupport Type: {support_type}\nName: {name}\nDescription: {description}\nReporter: {reporter}\nStatus: {status}\n")
        details_label.pack()

        toggle_button = tk.Button(ticket_window, text="Close Ticket" if status == "True" else "Open Ticket", command=toggle_ticket_status)
        toggle_button.pack()

        def edit_ticket():
            edit_window = tk.Toplevel(ticket_window)
            edit_window.title("Edit Ticket")

            tk.Label(edit_window, text="Ticket Number: " + str(ticket_number)).pack()

            tk.Label(edit_window, text="Support Type").pack()
            support_type_var = tk.StringVar()
            support_type_combobox = ttk.Combobox(edit_window, textvariable=support_type_var, state="readonly")
            support_type_combobox['values'] = ("Classroom", "General", "Software", "Hardware", "Other")
            support_type_combobox.set(support_type)
            support_type_combobox.pack()

            tk.Label(edit_window, text="Name").pack()
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, name)
            name_entry.pack()

            tk.Label(edit_window, text="Description").pack()
            description_entry = tk.Entry(edit_window)
            description_entry.insert(0, description)
            description_entry.pack()

            def validate_name_input(name):
                return re.match("^[A-Za-z\s]*$", name) and bool(name)

            def validate_desc_input(desc):
                return bool(desc)

            def save_changes():
                edited_support_type = support_type_var.get()
                edited_name = name_entry.get()
                edited_description = description_entry.get()

                if not validate_name_input(edited_name):
                    messagebox.showerror("Invalid Input", "Name should only contain letters (no special characters or numbers).")
                    return

                if not validate_desc_input(edited_description):
                    messagebox.showerror("Invalid Input", "Description must not be empty.")
                    return

                with open("GroupProject3/files/tickets.csv", 'r', newline='') as file:
                    rows = list(csv.reader(file))
                    for row in rows:
                        if row[0] == ticket_number:
                            row[1] = edited_support_type
                            row[2] = edited_name
                            row[3] = edited_description
                            break

                with open("GroupProject3/files/tickets.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

                edit_window.destroy()
                details_label.config(text=f"Ticket Number: {ticket_number}\nSupport Type: {edited_support_type}\nName: {edited_name}\nDescription: {edited_description}\nReporter: {reporter}\nStatus: {status}\n")
                refresh_treeview()

            save_button = tk.Button(edit_window, text="Save", command=save_changes)
            save_button.pack()

        edit_button = tk.Button(ticket_window, text="Edit", command=edit_ticket)
        edit_button.pack()
    
    def create_new_ticket():
        new_ticket_window = tk.Toplevel(dashboard_window)
        new_ticket_window.title("Create New Ticket")

        new_ticket_number = generate_unique_ticket_number(existing_ticket_numbers)
        tk.Label(new_ticket_window, text="Ticket Number: " + new_ticket_number).pack()

        tk.Label(new_ticket_window, text="Support Type").pack()
        support_type_var = tk.StringVar()
        support_type_combobox = ttk.Combobox(new_ticket_window, textvariable=support_type_var, state="readonly")
        support_type_combobox['values'] = ("Classroom", "General", "Software", "Hardware", "Other")
        support_type_combobox.pack()

        tk.Label(new_ticket_window, text="Name").pack()
        name_entry = tk.Entry(new_ticket_window)
        name_entry.pack()

        tk.Label(new_ticket_window, text="Description").pack()
        description_entry = tk.Entry(new_ticket_window)
        description_entry.pack()

        reporter_label = tk.Label(new_ticket_window, text="Reporter: " + current_username)
        reporter_label.pack()

        def validate_name_input(name):
            return re.match("^[A-Za-z\s]*$", name) and bool(name)
        
        def validate_desc_input(desc):
            return bool(desc)

        def save_new_ticket():
            support_type = support_type_var.get()
            if not support_type:
                messagebox.showerror("Invalid Input", "Please select a Support Type.")
                return
            name = name_entry.get()
            if not validate_name_input(name):
                messagebox.showerror("Invalid Input", "Name should only contain letters (no special characters or numbers).")
                return

            description = description_entry.get()
            if not validate_desc_input(description):
                messagebox.showerror("Invalid Input", "Description must not be empty.")
                return
            status = "True"  # Default status is True

            with open("GroupProject3/files/tickets.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([new_ticket_number, support_type, name, description, current_username, status])

            new_ticket_window.destroy()
            refresh_treeview()

        save_button = tk.Button(new_ticket_window, text="Save", command=save_new_ticket)
        save_button.pack()

    def search_ticket():
        search_window = tk.Toplevel(dashboard_window)
        search_window.title("Search Ticket")

        tk.Label(search_window, text="Enter Ticket Number:").pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()

        def validate_search_input(ticket_number):
            return re.match("^[0-9]+$", ticket_number) is not None

        def search():
            ticket_number = search_entry.get()
            if not validate_search_input(ticket_number):
                messagebox.showerror("Invalid Input", "Ticket number should only contain numbers.")
                return

            with open("GroupProject3/files/tickets.csv", newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if row[0] == ticket_number:
                        ticket_data = row
                        open_ticket_window(ticket_data)
                        search_window.destroy()
                        return
                messagebox.showerror("Ticket Not Found", "Ticket not found for the entered number.")

        search_button = tk.Button(search_window, text="Search", command=search)
        search_button.pack()

    def refresh_treeview():
        for row in table.get_children():
            table.delete(row)

        with open("GroupProject3/files/tickets.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row[5] == "True":
                    table.insert("", "end", values=row)

    def open_ticket_dashboard(selected_row):
        ticket_window = tk.Toplevel(dashboard_window)
        ticket_window.title("Ticket Details")
        ticket_number, support_type, name, description, reporter, status = selected_row

        details_label = tk.Label(ticket_window, text=f"Ticket Number: {ticket_number}\nSupport Type: {support_type}\nName: {name}\nDescription: {description}\nReporter: {reporter}\nStatus: {status}\n")
        details_label.pack()

    def on_double_click(event):
        item = table.selection()[0]
        open_ticket_dashboard(table.item(item)["values"])

    table = ttk.Treeview(dashboard_window, columns=("Ticket Number", "Support Type", "Name", "Description", "Reporter"))
    table.heading("#1", text="Ticket Number")
    table.heading("#2", text="Support Type")
    table.heading("#3", text="Name")
    table.heading("#4", text="Description")
    table.heading("#5", text="Reporter")

    with open("GroupProject3/files/tickets.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[5] == "True":
                table.insert("", "end", values=row)

    table.grid(row=1, column=0, columnspan=2, pady=10)

    new_ticket_button = tk.Button(dashboard_window, text="New Ticket", command=create_new_ticket)
    new_ticket_button.grid(row=2, column=0, pady=10)

    search_button = tk.Button(dashboard_window, text="Search Ticket", command=search_ticket)
    search_button.grid(row=2, column=1, pady=10)

    convert_to_json_button = tk.Button(dashboard_window, text="Convert To JSON", command=convert_to_json)
    convert_to_json_button.grid(row=2, column=0, columnspan=2, pady=10)

    logout = tk.Button(dashboard_window, text="Close Dashboard", command=logout)
    logout.grid(row=3, column=0, columnspan=2, pady=10)

    table.bind("<Double-1>", on_double_click)

    dashboard_window.mainloop()

login_window = tk.Tk()
login_window.title("Login")

login_window.geometry("370x300")
login_window.configure(padx=20, pady=20)

login_logo_image = tk.PhotoImage(file="GroupProject3/files/redlogo.png").subsample(2, 2)  
login_logo_label = tk.Label(login_window, image=login_logo_image)
login_logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

username_label = tk.Label(login_window, text="Username:")
username_entry = tk.Entry(login_window)
password_label = tk.Label(login_window, text="Password:")
password_entry = tk.Entry(login_window, show="*")

login_button = tk.Button(login_window, text="Login", command=login)

username_label.grid(row=1, column=0, padx=10, pady=10)
username_entry.grid(row=1, column=1, padx=10, pady=10)
password_label.grid(row=2, column=0, padx=10, pady=10)
password_entry.grid(row=2, column=1, padx=10, pady=10)
login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

login_window.mainloop()
