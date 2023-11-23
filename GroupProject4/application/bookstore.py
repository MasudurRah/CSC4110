import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import ttk
import csv

def customer_login():
    print("Customer Login Button Clicked")

def open_employee_login_window():
    employee_login_window = tk.Toplevel(root)
    employee_login_window.title("Employee Login")
    employee_login_window.geometry("400x350")

    if img:
        image_label = tk.Label(employee_login_window, image=img)
        image_label.pack(pady=10)

    username_label = tk.Label(employee_login_window, text="Username:")
    password_label = tk.Label(employee_login_window, text="Password:")
    username_entry = tk.Entry(employee_login_window)
    password_entry = tk.Entry(employee_login_window, show="*")

    login_button = tk.Button(employee_login_window, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), employee_login_window))

    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    login_button.pack(pady=10)

def login(username, password, window):
    with open("GroupProject4/files/user_credentials.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["user"] == username and row["pass"] == password:
                window.destroy()
                open_employee_dashboard()
                return

    messagebox.showerror("Error", "Invalid credentials")

def open_employee_dashboard():
    employee_dashboard_window = tk.Toplevel(root)
    employee_dashboard_window.title("Employee Dashboard")
    employee_dashboard_window.geometry("1250x500")

    if img:
        image_label = tk.Label(employee_dashboard_window, image=img)
        image_label.pack(pady=10)

    tree = ttk.Treeview(employee_dashboard_window)
    tree["columns"] = tuple(get_column_names("GroupProject4/files/books.csv"))

    tree["show"] = "headings"

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tree.insert("", tk.END, values=tuple(row[col] for col in tree["columns"]))

    def on_double_click(event):
        item = tree.selection()[0]
        row_data = tree.item(item, "values")
        show_details_window(row_data)

    tree.bind("<Double-1>", on_double_click)

    tree.pack(pady=10, padx=10)

    button_frame = tk.Frame(employee_dashboard_window)
    button_frame.pack(pady=10)

    button1 = tk.Button(button_frame, text="Button 1", command=lambda: print("Button 1 clicked"))
    button2 = tk.Button(button_frame, text="Button 2", command=lambda: print("Button 2 clicked"))
    button3 = tk.Button(button_frame, text="Button 3", command=lambda: print("Button 3 clicked"))

    button1.pack(side=tk.LEFT, padx=10)
    button2.pack(side=tk.LEFT, padx=10)
    button3.pack(side=tk.LEFT, padx=10)

    logout_button = tk.Button(employee_dashboard_window, text="Logout", command=lambda: logout(employee_dashboard_window))
    logout_button.pack(pady=10)

def logout(window):
    window.destroy()
    open_employee_login_window()

def get_column_names(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames

def show_details_window(row_data):
    details_window = tk.Toplevel(root)
    details_window.title("Row Details")

    for col, value in zip(get_column_names("GroupProject4/files/books.csv"), row_data):
        label = tk.Label(details_window, text=f"{col}: {value}")
        label.pack(pady=5)

root = tk.Tk()
root.title("Login App")
root.geometry("400x300")

image_path = "GroupProject4/files/shopping-basket.png"
try:
    img = PhotoImage(file=image_path)
    img = img.subsample(5)
except tk.TclError:
    print(f"Error: Image file '{image_path}' not found.")
    img = None

if img:
    image_label = tk.Label(root, image=img)
    image_label.pack(pady=10)

button_width = 20
button_height = 3
customer_button = tk.Button(root, text="Customer Login", command=customer_login, width=button_width, height=button_height, compound=tk.TOP)
employee_button = tk.Button(root, text="Employee Login", command=open_employee_login_window, width=button_width, height=button_height, compound=tk.TOP)

customer_button.pack(pady=5)
employee_button.pack(pady=5)

root.mainloop()
