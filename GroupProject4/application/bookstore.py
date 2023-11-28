import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import ttk
import csv
import re
import random

def customer_login():
    print("Customer Login Button Clicked")
    open_customer_login_window()

def open_customer_login_window():
    # Create a new window for customer login
    customer_login_window = tk.Toplevel(root)
    customer_login_window.title("Customer Login")
    customer_login_window.geometry("400x400")

    if img:
        image_label = tk.Label(customer_login_window, image=img)
        image_label.pack(pady=10)

    # Create labels and entry widgets for username and password
    username_label = tk.Label(customer_login_window, text="Username:")
    password_label = tk.Label(customer_login_window, text="Password:")
    username_entry = tk.Entry(customer_login_window)
    password_entry = tk.Entry(customer_login_window, show="*")  # Show asterisks for password

    # Create a login button
    login_button = tk.Button(customer_login_window, text="Login", command=lambda: customer_login_check(username_entry.get(), password_entry.get(), customer_login_window))

    # Create a register button
    register_button = tk.Button(customer_login_window, text="Register", command=open_registration_window)

    # Pack the widgets
    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    login_button.pack(pady=10)
    register_button.pack(pady=10)

def customer_login_check(username, password, window):
    # Check the credentials from the CSV file
    with open("GroupProject4/files/customer-info.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["user"] == username and row["pass"] == password:
                # Successful login, close the customer login window
                window.destroy()
                # Open a new blank window (you can customize this as needed)
                open_blank_window("Customer Dashboard")
                return

    # If no matching credentials found, show an error message
    response = messagebox.askquestion("Error", "Incorrect information. Would you like to register?")
    if response == 'yes':
        open_registration_window()

def open_registration_window():
    # Create a new window for customer registration
    registration_window = tk.Toplevel(root)
    registration_window.title("Customer Registration")
    registration_window.geometry("400x400")

    # Create labels and entry widgets for registration details
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

    # Create a dropdown menu for states
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
              "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
              "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
              "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
              "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    state_var = tk.StringVar()
    state_dropdown = ttk.Combobox(registration_window, textvariable=state_var, values=states)

    # Create a register button
    register_button = tk.Button(registration_window, text="Register", command=lambda: register_customer(username_entry.get(), password_entry.get(), email_entry.get(), address_entry.get(), zipcode_entry.get(), city_entry.get(), state_var.get(), registration_window))

    # Pack the widgets
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
    # Check if any field is empty
    if not (username and password and email and address and zipcode and city and state):
        messagebox.showerror("Error", "All fields must have a value")
        return

    # Validate email using regex
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        messagebox.showerror("Error", "Invalid email format")
        return

    # Validate zipcode using regex (5 digits)
    zipcode_regex = r'^\d{5}$'
    if not re.match(zipcode_regex, zipcode):
        messagebox.showerror("Error", "Invalid zipcode format (5 digits)")
        return

    # Check if the username is unique
    with open("GroupProject4/files/customer-info.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["user"] == username:
                messagebox.showerror("Error", "Username is already taken. Please choose a different one.")
                return

    # Save customer information to the CSV file
    with open("GroupProject4/files/customer-info.csv", "a", newline="") as file:
        fieldnames = ["username", "password", "email", "address", "zipcode", "city", "state"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Write the header only if the file is empty
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

    # Close the registration window
    window.destroy()
    # Open a new blank window (you can customize this as needed)
    open_blank_window("Registration Successful")

def open_blank_window(title):
    # Open a new blank window with two rows of three buttons each
    blank_window = tk.Toplevel(root)
    blank_window.title(title)
    blank_window.geometry("600x400")

    # Add the image label at the top middle
    if img:
        image_label = tk.Label(blank_window, image=img)
        image_label.pack(pady=10)

    best_sellers_label = tk.Label(blank_window, text="Best Sellers", font=("Helvetica", 16, "bold"))
    best_sellers_label.pack(pady=10)

    # Create the first row of buttons
    button_frame_row1 = tk.Frame(blank_window)
    button_frame_row1.pack(pady=10)

    # Read the CSV file and create buttons for the first three rows
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i < 3:
                button_text = f"{row['Book Name']}\n{row['Genre']}\n{row['Author']}"
                button = tk.Button(button_frame_row1, text=button_text, command=lambda r=row: apply_filter("Book Name", r["Book Name"]))
                button.pack(side=tk.LEFT, padx=10)

    # Create the second row of buttons
    button_frame_row2 = tk.Frame(blank_window)
    button_frame_row2.pack(pady=10)

    # Read the CSV file and create buttons for the next three rows
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if 3 <= i < 6:
                button_text = f"{row['Book Name']}\n{row['Genre']}\n{row['Author']}"
                button = tk.Button(button_frame_row2, text=button_text, command=lambda r=row: apply_filter("Book Name", r["Book Name"]))
                button.pack(side=tk.LEFT, padx=10)

    # Add a search button on the left-hand side
    search_button = tk.Button(blank_window, text="Search", command=open_search_window)
    search_button.pack(side=tk.LEFT, padx=10)

    cart_button = tk.Button(blank_window, text="Cart", command=open_cart_window)
    cart_button.pack(side=tk.LEFT, padx=10)

def open_cart_window():
    # Open the cart window to view items
    cart_window = tk.Toplevel(root)
    cart_window.title("Shopping Cart")
    cart_window.geometry("400x300")

    total_price = sum(details['price'] * details['quantity'] for details in cart.values())

    # Display the items in the cart
    for book_name, details in cart.items():
        tk.Label(cart_window, text=f"{book_name} - Quantity: {details['quantity']} - Price: ${details['price']}").pack()

    tk.Label(cart_window, text=f"Total Price: ${total_price:.2f}").pack(pady=5)

    # Add a button to complete the purchase
    complete_purchase_button = tk.Button(cart_window, text="Complete Purchase", command=lambda: complete_purchase(cart_window))
    complete_purchase_button.pack(pady=10)

def open_search_window():
    # Create a new window for search
    search_window = tk.Toplevel(root)
    search_window.title("Search")
    search_window.geometry("400x300")

    # Create radio buttons
    search_by_genre = tk.Radiobutton(search_window, text="Search by Genre", variable=1, value=1, command=lambda: load_filter_options("Genre"))
    search_by_book_name = tk.Radiobutton(search_window, text="Search by Book Name", variable=1, value=2, command=lambda: load_filter_options("Book Name"))
    search_by_author = tk.Radiobutton(search_window, text="Search by Author", variable=1, value=3, command=lambda: load_filter_options("Author"))

    # Pack the radio buttons
    search_by_genre.pack(pady=5)
    search_by_book_name.pack(pady=5)
    search_by_author.pack(pady=5)

def load_filter_options(column_name):
    # Load filter options based on the selected column_name
    # For simplicity, let's assume you have a CSV file with a column named 'Genre'
    # You can modify this function based on your actual CSV structure

    # Read unique values from the specified column
    options = set()
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            options.add(row[column_name])

    # Create a new window to display filter options
    filter_window = tk.Toplevel(root)
    filter_window.title(f"Filter by {column_name}")
    filter_window.geometry("300x200")

    # Create a drop-down menu with filter options
    filter_var = tk.StringVar()
    filter_dropdown = ttk.Combobox(filter_window, textvariable=filter_var, values=list(options))
    filter_dropdown.pack(pady=10)

    # Create a search button to apply the filter
    search_button = tk.Button(filter_window, text="Search", command=lambda: apply_filter(column_name, filter_var.get()))
    search_button.pack(pady=10)

def open_employee_login_window():
    # Create a new window for employee login
    employee_login_window = tk.Toplevel(root)
    employee_login_window.title("Employee Login")
    employee_login_window.geometry("400x350")

    # Create a label to display the image in the employee login window
    if img:
        image_label = tk.Label(employee_login_window, image=img)
        image_label.pack(pady=10)

    # Create labels and entry widgets for username and password
    username_label = tk.Label(employee_login_window, text="Username:")
    password_label = tk.Label(employee_login_window, text="Password:")
    username_entry = tk.Entry(employee_login_window)
    password_entry = tk.Entry(employee_login_window, show="*")  # Show asterisks for password

    # Create a login button
    login_button = tk.Button(employee_login_window, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), employee_login_window))

    # Pack the widgets
    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    login_button.pack(pady=10)

def apply_filter(column_name, filter_value):
    # Read the CSV file and filter rows based on the selected column and value
    matching_rows = []
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[column_name] == filter_value:
                matching_rows.append(row)

    # Check if there are multiple books with the same author or genre
    if len(matching_rows) > 1:
        # Create a new window to display book titles
        title_selection_window = tk.Toplevel(root)
        title_selection_window.title("Select Book Title")
        title_selection_window.geometry("400x300")

        # Create a listbox to display book titles
        title_listbox = tk.Listbox(title_selection_window, selectmode=tk.MULTIPLE)
        title_listbox.pack(pady=10)

        # Add book titles to the listbox
        for row in matching_rows:
            title_listbox.insert(tk.END, row['Book Name'])

        # Function to apply filter when titles are selected
        def apply_filter_on_titles():
            selected_titles = title_listbox.curselection()
            for index in selected_titles:
                selected_title = title_listbox.get(index)
                # Open a new window for each selected title
                details_window = tk.Toplevel(root)
                details_window.title("Row Details")
                details_window.geometry("700x300")

                # Find the selected title in matching rows
                selected_row = next((row for row in matching_rows if row['Book Name'] == selected_title), None)

                if selected_row:
                    # Display the book image on the left side of the window
                    image_path = f"GroupProject4/files/{selected_row['Book Name']}.png"
                    try:
                        global img  # Declare img as a global variable
                        img = PhotoImage(file=image_path)
                        img = img.subsample(3)  # Adjust the subsample factor as needed
                        image_label = tk.Label(details_window, image=img)
                        image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
                    except tk.TclError:
                        print(f"Error: Image file '{image_path}' not found.")

                    # Display the details in labels
                    tk.Label(details_window, text=f"Book Title: {selected_row['Book Name']}").grid(row=0, column=1, pady=5, sticky=tk.W)
                    tk.Label(details_window, text=f"Author: {selected_row['Author']}").grid(row=1, column=1, pady=5, sticky=tk.W)
                    tk.Label(details_window, text=f"Price: ${selected_row['Price']}").grid(row=2, column=1, pady=5, sticky=tk.W)

                    # Get and display the amount of inventory
                    inventory_label = tk.Label(details_window, text=f"Inventory: {selected_row['Inventory']}")
                    inventory_label.grid(row=3, column=1, pady=5, sticky=tk.W)

                    # Add "Buy" and "Sell" buttons
                    if int(selected_row['Inventory']) > 0:
                        buy_button = tk.Button(details_window, text="Buy", command=lambda name=selected_row['Book Name']: buy_book(name, details_window))
                    else:
                        buy_button = tk.Button(details_window, text="Sold Out", state=tk.DISABLED)

                    sell_button = tk.Button(details_window, text="Sell", command=sell_book)

                    buy_button.grid(row=4, column=1, pady=10, sticky=tk.W)
                    sell_button.grid(row=4, column=1, pady=10, sticky=tk.E)

        # Add a button to apply filter when titles are selected
        apply_filter_button = tk.Button(title_selection_window, text="Apply Filter", command=apply_filter_on_titles)
        apply_filter_button.pack(pady=10)

    else:
        # Open a new window for each matching row
        for row in matching_rows:
            details_window = tk.Toplevel(root)
            details_window.title("Row Details")
            details_window.geometry("700x300")

            # Display the book image on the left side of the window
            image_path = f"GroupProject4/files/{row['Book Name']}.png"
            try:
                global img  # Declare img as a global variable
                img = PhotoImage(file=image_path)
                img = img.subsample(3)  # Adjust the subsample factor as needed
                image_label = tk.Label(details_window, image=img)
                image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
            except tk.TclError:
                print(f"Error: Image file '{image_path}' not found.")

            # Display the details in labels
            tk.Label(details_window, text=f"Book Title: {row['Book Name']}").grid(row=0, column=1, pady=5, sticky=tk.W)
            tk.Label(details_window, text=f"Author: {row['Author']}").grid(row=1, column=1, pady=5, sticky=tk.W)
            tk.Label(details_window, text=f"Price: ${row['Price']}").grid(row=2, column=1, pady=5, sticky=tk.W)

            # Get and display the amount of inventory
            inventory_label = tk.Label(details_window, text=f"Inventory: {row['Inventory']}")
            inventory_label.grid(row=3, column=1, pady=5, sticky=tk.W)

            # Add "Buy" and "Sell" buttons
            if int(row['Inventory']) > 0:
                buy_button = tk.Button(details_window, text="Buy", command=lambda name=row['Book Name']: buy_book(name, details_window))
            else:
                buy_button = tk.Button(details_window, text="Sold Out", state=tk.DISABLED)

            sell_button = tk.Button(details_window, text="Sell", command=sell_book)

            buy_button.grid(row=4, column=1, pady=10, sticky=tk.W)
            sell_button.grid(row=4, column=1, pady=10, sticky=tk.E)


def buy_book(book_name, details_window):
    # Find the row in the CSV file for the given book name
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Book Name'] == book_name:
                inventory = int(row['Inventory'])
                break
        else:
            # Book not found, handle the error (you can customize this)
            messagebox.showerror("Error", f"Book not found: {book_name}")
            return

    # Calculate the quantity limit based on inventory
    quantity_limit = min(inventory, 5)

    # Create a new window for buying books
    buy_window = tk.Toplevel(root)
    buy_window.title("Buy Book")
    buy_window.geometry("300x200")

    # Display the book name in the buy window
    tk.Label(buy_window, text=f"Buy Book: {book_name}").pack(pady=10)

    # Create a dropdown for selecting quantity
    quantity_label = tk.Label(buy_window, text="Select Quantity:")
    quantity_var = tk.StringVar()
    quantity_var.set(1)  # Default quantity is 1
    quantity_dropdown = ttk.Combobox(buy_window, textvariable=quantity_var, values=list(range(1, quantity_limit + 1)))
    
    # Create buttons for adding to cart and cancel
    add_to_cart_button = tk.Button(buy_window, text="Add to Cart", command=lambda: add_to_cart(book_name, int(quantity_var.get()), buy_window))
    cancel_button = tk.Button(buy_window, text="Cancel", command=buy_window.destroy)

    # Pack the widgets
    quantity_label.pack(pady=5)
    quantity_dropdown.pack(pady=5)
    add_to_cart_button.pack(pady=10)
    cancel_button.pack(pady=10)

def add_to_cart(book_name, quantity, buy_window):
    # Open a new window for the shopping cart
    cart_window = tk.Toplevel(root)
    cart_window.title("Shopping Cart")
    cart_window.geometry("400x300")

    # Initialize or update the shopping cart dictionary
    if 'cart' not in globals():
        global cart
        cart = {}
    cart[book_name] = {'quantity': quantity, 'price': get_book_price(book_name)}

    # Display each book in the shopping cart with its price
    for book, details in cart.items():
        tk.Label(cart_window, text=f"{book} - Quantity: {details['quantity']} - Price: ${details['price']}").pack()

    # Calculate the total price and total price with tax
    total_price = sum(details['price'] * details['quantity'] for details in cart.values())
    total_price_with_tax = total_price * 1.06

    # Display the total price and total price with tax
    tk.Label(cart_window, text=f"Total Price: ${total_price:.2f}").pack(pady=5)
    tk.Label(cart_window, text=f"Total Price with Tax: ${total_price_with_tax:.2f}").pack(pady=5)

    # Add "Buy Now" and "Cancel" buttons
    buy_now_button = tk.Button(cart_window, text="Buy Now", command=lambda: complete_purchase(cart_window))
    cancel_button = tk.Button(cart_window, text="Cancel", command=cart_window.destroy)

    # Pack the buttons
    buy_now_button.pack(pady=10)
    cancel_button.pack(pady=10)

def get_book_price(book_name):
    # Retrieve the price of the book from the CSV file
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Book Name'] == book_name:
                return float(row['Price'])
    return 0.0  # Default to 0 if book not found

def complete_purchase(cart_window):
    # Update inventory and save changes to the CSV file
    update_inventory()

    # Read the latest transactionid from earnings.csv
    with open("GroupProject4/files/earnings.csv", "r") as earnings_file:
        earnings_data = list(csv.DictReader(earnings_file))
    
    latest_transactionid = earnings_data[-1]['transactionid']

    # Display a message box indicating the purchase is complete
    messagebox.showinfo("Purchase Complete", f"Your purchase is complete. It will be delivered to the address in your profile.\nTransaction ID: {latest_transactionid}")

    # Clear the shopping cart
    global cart
    cart = {}

    # Close the shopping cart window
    cart_window.destroy()

import random

def update_inventory():
    global cart

    # Update the inventory in the CSV file based on the items in the cart
    with open("GroupProject4/files/books.csv", "r") as file:
        books_data = list(csv.DictReader(file))

    for book_name, details in cart.items():
        for book in books_data:
            if book['Book Name'] == book_name:
                book['Inventory'] = str(int(book['Inventory']) - details['quantity'])
                break

    # Calculate earnings and update the earnings in the earnings CSV file
    units_sold = sum(details['quantity'] for details in cart.values())
    total_earned = sum(details['price'] * details['quantity'] for details in cart.values())
    total_spent = total_earned / 2

    # Read the current store fund value
    with open("GroupProject4/files/storefund.txt", "r") as store_fund_file:
        current_store_fund = float(store_fund_file.read().strip())

    # Convert the float value to an integer
    current_store_fund = int(current_store_fund)

    # Update the store fund
    updated_store_fund = current_store_fund + total_spent

    # Write the updated store fund value back to the storefund.txt file
    with open("GroupProject4/files/storefund.txt", "w") as store_fund_file:
        store_fund_file.write(str(updated_store_fund))

    # Generate a random 9-digit transactionid
    transactionid = str(random.randint(100000000, 999999999))

    # Add a new entry for the current transaction
    new_entry = {
        'store fund': str(updated_store_fund),
        'units': str(units_sold),
        'totalearned': str(total_earned),
        'totalspent': str(total_spent),
        'transactionid': transactionid  # Added transactionid
    }

    # Read existing earnings data
    with open("GroupProject4/files/earnings.csv", "r") as earnings_file:
        earnings_data = list(csv.DictReader(earnings_file))

    # Update the store fund, units, total earned, and total spent
    store_fund = updated_store_fund

    # Add a new entry for the current transaction
    new_entry = {
        'store fund': str(store_fund),
        'units': str(units_sold),
        'totalearned': str(total_earned),
        'totalspent': str(total_spent),
        'transactionid': transactionid  # Added transactionid
    }

    earnings_data.append(new_entry)

    # Write the updated earnings data back to the CSV file
    with open("GroupProject4/files/earnings.csv", "w", newline="") as earnings_file:
        fieldnames = earnings_data[0].keys()
        writer = csv.DictWriter(earnings_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(earnings_data)

    # Clear the cart after updating inventory
    cart = {}

    with open("GroupProject4/files/books.csv", "w", newline="") as file:
        fieldnames = books_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books_data)


def sell_book():
    sell_window = tk.Toplevel(root)
    sell_window.title("Sell Book")
    sell_window.geometry("300x200")
    tk.Label(sell_window, text="Sell Book.").pack(pady=20)



def login(username, password, window):
    # Check the credentials from the CSV file
    with open("GroupProject4/files/user_credentials.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["user"] == username and row["pass"] == password:
                # Successful login, close the employee login window
                window.destroy()
                # Open the employee dashboard
                open_employee_dashboard()
                return

    # If no matching credentials found, show an error message
    messagebox.showerror("Error", "Invalid credentials")

def open_employee_dashboard():
    # Create a new window for the employee dashboard
    employee_dashboard_window = tk.Toplevel(root)
    employee_dashboard_window.title("Employee Dashboard")
    employee_dashboard_window.geometry("1250x500")  # Set the size to 1250x500

    # Create a label to display the image in the employee dashboard window
    if img:
        image_label = tk.Label(employee_dashboard_window, image=img)
        image_label.pack(pady=10)

    # Create a Treeview for the table
    tree = ttk.Treeview(employee_dashboard_window)
    tree["columns"] = tuple(get_column_names("GroupProject4/files/books.csv"))

    # Hide the default ID column
    tree["show"] = "headings"

    # Add columns to the Treeview
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    # Populate the table with data from the CSV file
    with open("GroupProject4/files/books.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tree.insert("", tk.END, values=tuple(row[col] for col in tree["columns"]))

    # Handle double-click events
    def on_double_click(event):
        item = tree.selection()[0]
        row_data = tree.item(item, "values")
        show_details_window(row_data)

    tree.bind("<Double-1>", on_double_click)

    # Add the Treeview to the window with padding
    tree.pack(pady=10, padx=10)

    # Add three buttons that open a blank window when clicked
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


    # Add a logout button
    logout_button = tk.Button(employee_dashboard_window, text="Logout", command=lambda: logout(employee_dashboard_window))
    logout_button.pack(pady=10)

def logout(window):
    # Close the employee dashboard window
    window.destroy()
    # Open the employee login window
    open_employee_login_window()

def get_column_names(file_path):
    # Extract column names from the CSV file
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames

def show_details_window(row_data):
    # Create a new window to show details of the selected row
    details_window = tk.Toplevel(root)
    details_window.title("Row Details")

    # Display the details in labels
    for col, value in zip(get_column_names("GroupProject4/files/books.csv"), row_data):
        label = tk.Label(details_window, text=f"{col}: {value}")
        label.pack(pady=5)

# Create the main window with a larger size
root = tk.Tk()
root.title("Login App")
root.geometry("400x300")  # Set the size to 400x300

# Load the image
image_path = "GroupProject4/files/shopping-basket.png"
try:
    img = PhotoImage(file=image_path)
    # Resize the image
    img = img.subsample(5)  # Adjust the subsample factor as needed
except tk.TclError:
    print(f"Error: Image file '{image_path}' not found.")
    img = None

# Create a label to display the image
if img:
    image_label = tk.Label(root, image=img)
    image_label.pack(pady=10)

# Create the buttons with increased size
button_width = 20
button_height = 3
customer_button = tk.Button(root, text="Customer Login", command=customer_login, width=button_width, height=button_height, compound=tk.TOP)
employee_button = tk.Button(root, text="Employee Login", command=open_employee_login_window, width=button_width, height=button_height, compound=tk.TOP)

# Pack the buttons
customer_button.pack(pady=5)
employee_button.pack(pady=5)

# Start the main loop
root.mainloop()
