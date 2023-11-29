import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import ttk
import csv
import re
import random

img = None

def customer_login():
    open_customer_login_window()

def open_customer_login_window():
    customer_login_window = tk.Toplevel(root)
    customer_login_window.title("Customer Login")
    customer_login_window.geometry("400x400")

    if img:
        image_label = tk.Label(customer_login_window, image=img)
        image_label.pack(pady=10)

    username_label = tk.Label(customer_login_window, text="Username:")
    password_label = tk.Label(customer_login_window, text="Password:")
    username_entry = tk.Entry(customer_login_window)
    password_entry = tk.Entry(customer_login_window, show="*")

    login_button = tk.Button(customer_login_window, text="Login", command=lambda: customer_login_check(username_entry.get(), password_entry.get(), customer_login_window))

    register_button = tk.Button(customer_login_window, text="Register", command=open_registration_window)

    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    login_button.pack(pady=10)
    register_button.pack(pady=10)

def customer_login_check(username, password, window):
    with open("GroupProject4/files/customer-info.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["user"] == username and row["pass"] == password:
                window.destroy()
                open_blank_window("Customer Dashboard")
                return

    response = messagebox.askquestion("Error", "Incorrect information. Would you like to register?")
    if response == 'yes':
        open_registration_window()

def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Customer Registration")
    registration_window.geometry("400x550")

    username_label = tk.Label(registration_window, text="Username:")
    password_label = tk.Label(registration_window, text="Password:")
    email_label = tk.Label(registration_window, text="Email:")
    address_label = tk.Label(registration_window, text="Address:")
    zipcode_label = tk.Label(registration_window, text="Zipcode:")
    city_label = tk.Label(registration_window, text="City:")
    state_label = tk.Label(registration_window, text="State:")

    username_entry = tk.Entry(registration_window)
    password_entry = tk.Entry(registration_window, show="*")
    email_entry = tk.Entry(registration_window)
    address_entry = tk.Entry(registration_window)
    zipcode_entry = tk.Entry(registration_window)
    city_entry = tk.Entry(registration_window)

    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
              "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
              "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
              "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
              "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    state_var = tk.StringVar()
    state_dropdown = ttk.Combobox(registration_window, textvariable=state_var, values=states)

    register_button = tk.Button(registration_window, text="Register", command=lambda: register_customer(username_entry.get(), password_entry.get(), email_entry.get(), address_entry.get(), zipcode_entry.get(), city_entry.get(), state_var.get(), registration_window))

    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    email_label.pack(pady=5)
    email_entry.pack(pady=5)
    address_label.pack(pady=5)
    address_entry.pack(pady=5)
    zipcode_label.pack(pady=5)
    zipcode_entry.pack(pady=5)
    city_label.pack(pady=5)
    city_entry.pack(pady=5)
    state_label.pack(pady=5)
    state_dropdown.pack(pady=5)
    register_button.pack(pady=10)

def register_customer(username, password, email, address, zipcode, city, state, window):
    if not (username and password and email and address and zipcode and city and state):
        messagebox.showerror("Error", "All fields must have a value")
        return

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        messagebox.showerror("Error", "Invalid email format")
        return

    zipcode_regex = r'^\d{5}$'
    if not re.match(zipcode_regex, zipcode):
        messagebox.showerror("Error", "Invalid zipcode format (5 digits)")
        return

    with open("GroupProject4/files/customer-info.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["user"] == username:
                messagebox.showerror("Error", "Username is already taken. Please choose a different one.")
                return

    with open("GroupProject4/files/customer-info.csv", "a", newline="") as file:
        fieldnames = ["username", "password", "email", "address", "zipcode", "city", "state"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({
            "username": username,
            "password": password,
            "email": email,
            "address": address,
            "zipcode": zipcode,
            "city": city,
            "state": state
        })

    window.destroy()
    open_blank_window("Registration Successful")

def open_blank_window(title):
    global img
    blank_window = tk.Toplevel(root)
    blank_window.title(title)
    blank_window.geometry("600x400")

    best_sellers_label = tk.Label(blank_window, text="Best Sellers", font=("Helvetica", 16, "bold"))
    best_sellers_label.pack(pady=10)

    if img:
        image_label = tk.Label(blank_window, image=img)
        image_label.pack(pady=10)

    button_frame_row1 = tk.Frame(blank_window)
    button_frame_row1.pack(pady=10)

    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i < 3:
                button_text = f"{row['Book Name']}\n{row['Genre']}\n{row['Author']}"
                button = tk.Button(button_frame_row1, text=button_text, command=lambda r=row: apply_filter("Book Name", r["Book Name"]))
                button.pack(side=tk.LEFT, padx=10)

    button_frame_row2 = tk.Frame(blank_window)
    button_frame_row2.pack(pady=10)

    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if 3 <= i < 6:
                button_text = f"{row['Book Name']}\n{row['Genre']}\n{row['Author']}"
                button = tk.Button(button_frame_row2, text=button_text, command=lambda r=row: apply_filter("Book Name", r["Book Name"]))
                button.pack(side=tk.LEFT, padx=10)

    search_button = tk.Button(blank_window, text="Search", command=open_search_window)
    search_button.pack(side=tk.LEFT, padx=10)

    cart_button = tk.Button(blank_window, text="Cart", command=open_cart_window)
    cart_button.pack(side=tk.LEFT, padx=10)

    logout_button = tk.Button(blank_window, text="Logout", command=lambda: [blank_window.destroy(), customer_login()])
    logout_button.pack(pady=10)

def open_cart_window():
    cart_window = tk.Toplevel(root)
    cart_window.title("Shopping Cart")
    cart_window.geometry("400x300")

    total_price = sum(details['price'] * details['quantity'] for details in cart.values())

    for book_name, details in cart.items():
        tk.Label(cart_window, text=f"{book_name} - Quantity: {details['quantity']} - Price: ${details['price']}").pack()

    tk.Label(cart_window, text=f"Total Price: ${total_price:.2f}").pack(pady=5)

    complete_purchase_button = tk.Button(cart_window, text="Complete Purchase", command=lambda: complete_purchase(cart_window))
    complete_purchase_button.pack(pady=10)

def open_search_window():
    search_window = tk.Toplevel(root)
    search_window.title("Search")
    search_window.geometry("400x300")

    search_by_genre = tk.Radiobutton(search_window, text="Search by Genre", variable=1, value=1, command=lambda: load_filter_options("Genre"))
    search_by_book_name = tk.Radiobutton(search_window, text="Search by Book Name", variable=1, value=2, command=lambda: load_filter_options("Book Name"))
    search_by_author = tk.Radiobutton(search_window, text="Search by Author", variable=1, value=3, command=lambda: load_filter_options("Author"))

    search_by_genre.pack(pady=5)
    search_by_book_name.pack(pady=5)
    search_by_author.pack(pady=5)

def load_filter_options(column_name):
    options = set()
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            options.add(row[column_name])

    filter_window = tk.Toplevel(root)
    filter_window.title(f"Filter by {column_name}")
    filter_window.geometry("300x200")

    filter_var = tk.StringVar()
    filter_dropdown = ttk.Combobox(filter_window, textvariable=filter_var, values=list(options))
    filter_dropdown.pack(pady=10)

    search_button = tk.Button(filter_window, text="Search", command=lambda: apply_filter(column_name, filter_var.get()))
    search_button.pack(pady=10)

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

def apply_filter(column_name, filter_value):
    matching_rows = []
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[column_name] == filter_value:
                matching_rows.append(row)

    if len(matching_rows) > 1:
        title_selection_window = tk.Toplevel(root)
        title_selection_window.title("Select Book Title")
        title_selection_window.geometry("400x300")

        title_listbox = tk.Listbox(title_selection_window, selectmode=tk.MULTIPLE)
        title_listbox.pack(pady=10)

        for row in matching_rows:
            title_listbox.insert(tk.END, row['Book Name'])

        def apply_filter_on_titles():
            selected_titles = title_listbox.curselection()
            for index in selected_titles:
                selected_title = title_listbox.get(index)
                details_window = tk.Toplevel(root)
                details_window.title("Row Details")
                details_window.geometry("700x300")

                selected_row = next((row for row in matching_rows if row['Book Name'] == selected_title), None)

                if selected_row:
                    image_path = f"GroupProject4/files/{selected_row['Book Name']}.png"
                    try:
                        img_local = PhotoImage(file=image_path)
                        img_local = img_local.subsample(3)
                        image_label = tk.Label(details_window, image=img_local)
                        image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
                        image_label.image = img_local
                    except tk.TclError:
                        print(f"Error: Image file '{image_path}' not found.")

                    tk.Label(details_window, text=f"Book Title: {selected_row['Book Name']}").grid(row=0, column=1, pady=5, sticky=tk.W)
                    tk.Label(details_window, text=f"Author: {selected_row['Author']}").grid(row=1, column=1, pady=5, sticky=tk.W)
                    tk.Label(details_window, text=f"Price: ${selected_row['Price']}").grid(row=2, column=1, pady=5, sticky=tk.W)

                    inventory_label = tk.Label(details_window, text=f"Inventory: {selected_row['Inventory']}")
                    inventory_label.grid(row=3, column=1, pady=5, sticky=tk.W)

                    if int(selected_row['Inventory']) > 0:
                        buy_button = tk.Button(details_window, text="Buy", command=lambda name=selected_row['Book Name']: buy_book(name, details_window))
                    else:
                        buy_button = tk.Button(details_window, text="Sold Out", state=tk.DISABLED)

                    sell_button = tk.Button(details_window, text="Sell", command=lambda title=row['Book Name']: sell_book(title))#

                    buy_button.grid(row=4, column=1, pady=10, sticky=tk.W)
                    sell_button.grid(row=4, column=1, pady=10, sticky=tk.E)

        apply_filter_button = tk.Button(title_selection_window, text="Apply Filter", command=apply_filter_on_titles)
        apply_filter_button.pack(pady=10)

    else:
        for row in matching_rows:
            details_window = tk.Toplevel(root)
            details_window.title("Row Details")
            details_window.geometry("700x300")

            image_path = f"GroupProject4/files/{row['Book Name']}.png"
            try:
                img_local = PhotoImage(file=image_path)
                img_local = img_local.subsample(3)
                image_label = tk.Label(details_window, image=img_local)
                image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
                image_label.image = img_local
            except tk.TclError:
                print(f"Error: Image file '{image_path}' not found.")

            tk.Label(details_window, text=f"Book Title: {row['Book Name']}").grid(row=0, column=1, pady=5, sticky=tk.W)
            tk.Label(details_window, text=f"Author: {row['Author']}").grid(row=1, column=1, pady=5, sticky=tk.W)
            tk.Label(details_window, text=f"Price: ${row['Price']}").grid(row=2, column=1, pady=5, sticky=tk.W)

            inventory_label = tk.Label(details_window, text=f"Inventory: {row['Inventory']}")
            inventory_label.grid(row=3, column=1, pady=5, sticky=tk.W)

            if int(row['Inventory']) > 0:
                buy_button = tk.Button(details_window, text="Buy", command=lambda name=row['Book Name']: buy_book(name, details_window))
            else:
                buy_button = tk.Button(details_window, text="Sold Out", state=tk.DISABLED)

            sell_button = tk.Button(details_window, text="Sell", command=lambda title=row['Book Name']: sell_book(title))

            buy_button.grid(row=4, column=1, pady=10, sticky=tk.W)
            sell_button.grid(row=4, column=1, pady=10, sticky=tk.E)


def buy_book(book_name, details_window):
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Book Name'] == book_name:
                inventory = int(row['Inventory'])
                break
        else:
            messagebox.showerror("Error", f"Book not found: {book_name}")
            return

    quantity_limit = min(inventory, 5)

    buy_window = tk.Toplevel(root)
    buy_window.title("Buy Book")
    buy_window.geometry("300x200")

    tk.Label(buy_window, text=f"Buy Book: {book_name}").pack(pady=10)

    quantity_label = tk.Label(buy_window, text="Select Quantity:")
    quantity_var = tk.StringVar()
    quantity_var.set(1)
    quantity_dropdown = ttk.Combobox(buy_window, textvariable=quantity_var, values=list(range(1, quantity_limit + 1)))
    
    add_to_cart_button = tk.Button(buy_window, text="Add to Cart", command=lambda: add_to_cart(book_name, int(quantity_var.get()), buy_window))
    cancel_button = tk.Button(buy_window, text="Cancel", command=buy_window.destroy)

    quantity_label.pack(pady=5)
    quantity_dropdown.pack(pady=5)
    add_to_cart_button.pack(pady=10)
    cancel_button.pack(pady=10)

def add_to_cart(book_name, quantity, buy_window):
    cart_window = tk.Toplevel(root)
    cart_window.title("Shopping Cart")
    cart_window.geometry("400x300")

    if 'cart' not in globals():
        global cart
        cart = {}
    cart[book_name] = {'quantity': quantity, 'price': get_book_price(book_name)}

    for book, details in cart.items():
        tk.Label(cart_window, text=f"{book} - Quantity: {details['quantity']} - Price: ${details['price']}").pack()

    total_price = sum(details['price'] * details['quantity'] for details in cart.values())
    total_price_with_tax = total_price * 1.06

    tk.Label(cart_window, text=f"Total Price: ${total_price:.2f}").pack(pady=5)
    tk.Label(cart_window, text=f"Total Price with Tax: ${total_price_with_tax:.2f}").pack(pady=5)

    buy_now_button = tk.Button(cart_window, text="Buy Now", command=lambda: complete_purchase(cart_window))
    cancel_button = tk.Button(cart_window, text="Cancel", command=cart_window.destroy)

    buy_now_button.pack(pady=10)
    cancel_button.pack(pady=10)

def get_book_price(book_name):
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Book Name'] == book_name:
                return float(row['Price'])
    return 0.0

def complete_purchase(cart_window):
    update_inventory()

    with open("GroupProject4/files/earnings.csv", "r") as earnings_file:
        earnings_data = list(csv.DictReader(earnings_file))
    
    latest_transactionid = earnings_data[-1]['transactionid']

    messagebox.showinfo("Purchase Complete", f"Your purchase is complete. It will be delivered to the address in your profile.\nTransaction ID: {latest_transactionid}")

    global cart
    cart = {}

    cart_window.destroy()


def update_inventory():
    global cart

    with open("GroupProject4/files/books.csv", "r") as file:
        books_data = list(csv.DictReader(file))

    for book_name, details in cart.items():
        for book in books_data:
            if book['Book Name'] == book_name:
                book['Inventory'] = str(int(book['Inventory']) - details['quantity'])
                break

    units_sold = sum(details['quantity'] for details in cart.values())
    total_earned = sum(details['price'] * details['quantity'] for details in cart.values())
    total_spent = total_earned / 2

    with open("GroupProject4/files/storefund.txt", "r") as store_fund_file:
        current_store_fund = float(store_fund_file.read().strip())

    current_store_fund = int(current_store_fund)

    updated_store_fund = current_store_fund + total_earned

    with open("GroupProject4/files/storefund.txt", "w") as store_fund_file:
        store_fund_file.write(str(updated_store_fund))

    transactionid = str(random.randint(100000000, 999999999))

    new_entry = {
        'store fund': str(updated_store_fund),
        'units': str(units_sold),
        'totalearned': str(total_earned),
        'totalspent': str(total_spent),
        'transactionid': transactionid
    }

    with open("GroupProject4/files/earnings.csv", "r") as earnings_file:
        earnings_data = list(csv.DictReader(earnings_file))

    store_fund = updated_store_fund

    new_entry = {
        'store fund': str(store_fund),
        'units': str(units_sold),
        'totalearned': str(total_earned),
        'totalspent': str(total_spent),
        'transactionid': transactionid
    }

    earnings_data.append(new_entry)

    with open("GroupProject4/files/earnings.csv", "w", newline="") as earnings_file:
        fieldnames = earnings_data[0].keys()
        writer = csv.DictWriter(earnings_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(earnings_data)

    cart = {}

    with open("GroupProject4/files/books.csv", "w", newline="") as file:
        fieldnames = books_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books_data)


def sell_book(book_title):
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Book Name'] == book_title:
                inventory = int(row['Inventory'])
                price = float(row['Price'])
                break
        else:
            messagebox.showerror("Error", f"Book not found: {book_title}")
            return

    quantity_limit = min(inventory, 5)

    sell_window = tk.Toplevel(root)
    sell_window.title(f"Sell Book: {book_title}")
    sell_window.geometry("300x300")

    tk.Label(sell_window, text=f"Sell Book: {book_title}").pack(pady=10)

    quantity_label = tk.Label(sell_window, text="Select Quantity:")
    quantity_var = tk.StringVar()
    quantity_var.set("1")  # Default quantity is 1
    quantity_values = [str(i) for i in range(1, 6)]
    quantity_dropdown = ttk.Combobox(sell_window, textvariable=quantity_var, values=quantity_values)

    price_label = tk.Label(sell_window, text=f"Price per Book: ${price / 2:.2f}")

    total_price_var = tk.StringVar()
    total_price_label = tk.Label(sell_window, textvariable=total_price_var)

    def update_total_price(*args):
        selected_quantity = int(quantity_var.get())
        total_price = (price / 2) * selected_quantity
        total_price_var.set(f"Total Price: ${total_price:.2f}")

    quantity_var.trace_add("write", update_total_price)

    confirm_button = tk.Button(sell_window, text="Confirm Sale", command=lambda: confirm_sale(book_title, int(quantity_var.get()), price, sell_window))
    cancel_button = tk.Button(sell_window, text="Cancel", command=sell_window.destroy)

    quantity_label.pack(pady=5)
    quantity_dropdown.pack(pady=5)
    price_label.pack(pady=5)
    total_price_label.pack(pady=5)
    confirm_button.pack(pady=10)
    cancel_button.pack(pady=10)

def confirm_sale(book_title, quantity, price, sell_window):
    with open("GroupProject4/files/storefund.txt", "r") as fund_file:
        store_fund = float(fund_file.read().strip())

    total_amount = quantity * (price / 2)

    new_store_fund = store_fund - total_amount

    with open("GroupProject4/files/books.csv", "r") as file:
        books_data = list(csv.DictReader(file))

    for book in books_data:
        if book['Book Name'] == book_title:
            book['Inventory'] = str(int(book['Inventory']) + quantity)
            break

    with open("GroupProject4/files/books.csv", "w", newline="") as file:
        fieldnames = books_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books_data)

    with open("GroupProject4/files/storefund.txt", "w") as fund_file:
        fund_file.write(f"{new_store_fund:.2f}")

    transaction_id = generate_unique_transaction_id()

    update_earnings_csv(transaction_id, quantity, total_amount)

    sell_window.destroy()

    messagebox.showinfo("Sale Confirmation", f"You have successfully sold {quantity} copies of {book_title} for a total of ${total_amount:.2f}.\nTransaction ID: {transaction_id}")

def generate_unique_transaction_id():
    transaction_id = str(random.randint(100000000, 999999999))

    with open("GroupProject4/files/earnings.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if transaction_id == row[4]:
                return generate_unique_transaction_id()

    return transaction_id

def update_earnings_csv(transaction_id, quantity, total_price):
    previous_store_fund = get_previous_store_fund()

    new_store_fund = previous_store_fund - total_price
    total_earned = 0
    total_spent = total_price

    with open("GroupProject4/files/earnings.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([new_store_fund, quantity, total_earned, total_spent, transaction_id])

def get_previous_store_fund():
    try:
        with open("GroupProject4/files/earnings.csv", "r") as file:
            reader = csv.reader(file)
            last_row = None
            for row in reader:
                last_row = row
            if last_row:
                return float(last_row[0])
    except FileNotFoundError:
        return 0.0

def initialize_earnings_csv():
    try:
        with open("GroupProject4/files/earnings.csv", "r") as file:
            pass
    except FileNotFoundError:
        with open("GroupProject4/files/earnings.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Store Fund", "Units Sold", "Total Earned", "Total Spent", "Transaction ID"])

initialize_earnings_csv()


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

    def buyInventory():
        blank_window = tk.Toplevel(employee_dashboard_window)
        blank_window.title("Buy Inventory")
        blank_window.geometry("300x200")
        tk.Label(blank_window, text="Buy Inventory.").pack(pady=20)

    def viewearnings():
        blank_window = tk.Toplevel(employee_dashboard_window)
        blank_window.title("Earnings")
        blank_window.geometry("300x200")
        tk.Label(blank_window, text="THIS WINDOW SHOWS EARNINGS").pack(pady=20)

    def buttonk3():
        blank_window = tk.Toplevel(employee_dashboard_window)
        blank_window.title("Blank Window")
        blank_window.geometry("300x200")
        tk.Label(blank_window, text="This is window 3.").pack(pady=20)

    button1 = tk.Button(button_frame, text="Buy Inventory", command=buyInventory)
    button2 = tk.Button(button_frame, text="View Earnings", command=viewearnings)

    button1.pack(side=tk.LEFT, padx=10)
    button2.pack(side=tk.LEFT, padx=10)

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
