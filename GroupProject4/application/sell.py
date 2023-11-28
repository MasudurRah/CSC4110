import tkinter as tk
from tkinter import ttk, messagebox
import csv

def read_books():
    """
    Opening a csv file and putting the data into a dictionary. Keys are the book name and the info for it are the values. 
    retruns a dict
    """
    with open('books.csv', 'r') as booksFile:
        booksReader = csv.DictReader(booksFile)
        books = {row['Book Name']: {'price': float(row['Price']), 'quantity': int(row['Inventory'])} for row in booksReader}
    return books

def write_books(books):
    """
    updating the info for the book that is given
    adding a value for how many the user has sold to the store, resets to 0 after read function is called
    """
    with open('books.csv', 'w', newline='') as booksFile:
        tags = ['Book Name', 'Author', 'Inventory', 'ISBN', 'Genre', 'Price']
        booksWriter = csv.DictWriter(booksFile, fieldnames=tags)
        booksWriter.writeheader()
        for title, info in books.items():
            booksWriter.writerow({'Book Name': title, 'Author': '', 'Inventory': info['quantity'], 'ISBN': '', 'Genre': '', 'Price': info['price'], 'sold': info.get('sold', 0)})

#reading and updating the store funds
def read_store_fund():
    with open('storefund.txt', 'r') as storeFile:
        store_fund = float(storeFile.read())
    return store_fund

def write_store_fund(store_fund):
    with open('storefund.txt', 'w') as storeFile:
        storeFile.write(str(store_fund))

def sell_book(title, quantity=1, sell_window=None):
    books = read_books()
    store_fund = read_store_fund()


    """
    checks if book is in our csv file
    makes sure they haven't sold more than 5 books and trying to sell more than 5 books
    calculations for selling the book
    updating store_funds
    """
    if title in books:
        if books[title].get('sold', 0) < 5 and quantity <= 5:
            buy_price = books[title]['price'] / 2
            buy_price *= quantity
            books[title]['quantity'] += quantity
            books[title]['sold'] = books[title].get('sold', 0) + quantity

            store_fund -= buy_price

            # Write back the updated information
            write_books(books)
            write_store_fund(store_fund)

            print(f"You sold '{quantity}' '{title}' for ${buy_price}.\nThank you for your patronage.\nStore fund: ${store_fund}.")

            if sell_window:
                sell_window.destroy()
        else:
            print(f"You've reached the sell limit for '{title}'.")
    else:
        print(f"Sorry, '{title}' is not a book that we can purchase from you.")

def create_sell_window(title, quantity):
    sell_window = tk.Toplevel(root)
    sell_window.title("Sell Book")
    sell_window.geometry("300x200")

    tk.Label(sell_window, text=f"Sell Book: {title}").pack(pady=10)

    quantity_label = tk.Label(sell_window, text="Select Quantity:")
    quantity_var = tk.StringVar()
    quantity_dropdown = ttk.Combobox(sell_window, textvariable=quantity_var, values=list(range(1, quantity + 1)))

    sell_button = tk.Button(sell_window, text="Sell", command=lambda: sell_book(title, int(quantity_var.get()), sell_window))
    cancel_button = tk.Button(sell_window, text="Cancel", command=sell_window.destroy)

    quantity_label.pack(pady=5)
    quantity_dropdown.pack(pady=5)
    sell_button.pack(pady=10)
    cancel_button.pack(pady=10)