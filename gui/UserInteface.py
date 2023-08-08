import tkinter as tk
import sqlite3

# This is a bad implementation of this. It would be smarter to only connect to the database once and then pass the connection object around to the functions that need it.
# Also everything is in one file. It would be better to split this into multiple files and use classes to encapsulate the functionality.


def populate_list():
    listbox.delete(0, tk.END)  # Clear the existing items
    for item in get_items_from_database():
        listbox.insert(tk.END, item)

def add_item():
    item = entry.get()
    if item:
        insert_item_into_database(item)
        populate_list()

def remove_item():
    selected_indices = listbox.curselection()
    for index in reversed(selected_indices):
        delete_item_from_database(listbox.get(index))
    populate_list()

def create_database():
    conn = sqlite3.connect('list_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, item TEXT)''')
    conn.commit()
    conn.close()

def insert_item_into_database(item):
    conn = sqlite3.connect('list_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO items (item) VALUES (?)", (item,))
    conn.commit()
    conn.close()

def delete_item_from_database(item):
    conn = sqlite3.connect('list_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE item=?", (item,))
    conn.commit()
    conn.close()

def get_items_from_database():
    conn = sqlite3.connect('list_data.db')
    c = conn.cursor()
    c.execute("SELECT item FROM items")
    items = [row[0] for row in c.fetchall()]
    conn.close()
    return items

root = tk.Tk()
root.title("Scrollable List with SQLite Backend")

create_database()  # Create the SQLite database and table if they don't exist

listbox = tk.Listbox(root)
listbox.pack(padx=10, pady=10)

entry = tk.Entry(root)
entry.pack(padx=10, pady=5)

add_button = tk.Button(root, text="Add Item", command=add_item)
add_button.pack(pady=5)

remove_button = tk.Button(root, text="Remove Selected", command=remove_item)
remove_button.pack(pady=5)

populate_list()  # Load data from the database and populate the list

root.mainloop()