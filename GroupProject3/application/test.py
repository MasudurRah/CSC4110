import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import random

def check_credentials(username, password):
    return username == "ok" and password == "password"

def generate_unique_ticket_number(existing_ticket_numbers):
    while True:
        new_ticket_number = str(random.randint(10000, 99999))
        if new_ticket_number not in existing_ticket_numbers:
            existing_ticket_numbers.add(new_ticket_number)
            return new_ticket_number

existing_ticket_numbers = set()
with open("GroupProject3/tickets.csv", newline='') as csvfile:
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

def open_dashboard():
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")

    def open_ticket_window(selected_row):
        ticket_window = tk.Toplevel(dashboard_window)
        ticket_window.title("Ticket Details")
        ticket_number = selected_row[0]
        support_type = selected_row[1]
        name = selected_row[2]
        description = selected_row[3]
        reporter = selected_row[4]
        details_label = tk.Label(ticket_window, text=f"Ticket Number: {ticket_number}\nSupport Type: {support_type}\nName: {name}\nDescription: {description}\nReporter: {reporter}")
        details_label.pack()

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

        def save_new_ticket():
            support_type = support_type_var.get()
            name = name_entry.get()
            description = description_entry.get()

            with open("GroupProject3/tickets.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([new_ticket_number, support_type, name, description, current_username])

            new_ticket_window.destroy()
            refresh_treeview()

        save_button = tk.Button(new_ticket_window, text="Save", command=save_new_ticket)
        save_button.pack()

    def refresh_treeview():
        for row in table.get_children():
            table.delete(row)

        with open("GroupProject3/tickets.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                table.insert("", "end", values=row)

    def on_double_click(event):
        item = table.selection()[0]
        open_ticket_window(table.item(item)["values"])

    table = ttk.Treeview(dashboard_window, columns=("Ticket Number", "Support Type", "Name", "Description", "Reporter"))
    table.heading("#1", text="Ticket Number")
    table.heading("#2", text="Support Type")
    table.heading("#3", text="Name")
    table.heading("#4", text="Description")
    table.heading("#5", text="Reporter")

    with open("GroupProject3/tickets.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            table.insert("", "end", values=row)

    new_ticket_button = tk.Button(dashboard_window, text="New Ticket", command=create_new_ticket)

    table.bind("<Double-1>", on_double_click)

    table.pack()
    new_ticket_button.pack()

login_window = tk.Tk()
login_window.title("Login")

username_label = tk.Label(login_window, text="Username:")
username_entry = tk.Entry(login_window)
password_label = tk.Label(login_window, text="Password:")
password_entry = tk.Entry(login_window, show="*")

login_button = tk.Button(login_window, text="Login", command=login)

username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry.grid(row=0, column=1, padx=10, pady=10)
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry.grid(row=1, column=1, padx=10, pady=10)
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

login_window.mainloop()
