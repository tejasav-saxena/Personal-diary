import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os

# Global variable to store the username
username = ""

# Function to set the username
def set_username():
    global username
    username = name_entry.get().strip()
    if not username:
        messagebox.showwarning("Warning", "Please enter your name.")
        return
    
    # Create user directory if not exists
    user_dir = f"diary_entries/{username}"
    os.makedirs(user_dir, exist_ok=True)
    
    username_label.config(text=f"Welcome, {username}!")
    name_entry.config(state='disabled')
    set_username_button.config(state='disabled')
    update_entry_dates()  # Update available entries

# Function to reset the username
def reset_username():
    global username
    username = ""
    name_entry.config(state='normal')
    name_entry.delete(0, 'end')
    set_username_button.config(state='normal')
    username_label.config(text="")
    entry_dates_combobox['values'] = []  # Clear past entries list
    text_box.delete("1.0", "end")

# Function to save the diary entry
def save_entry():
    entry = text_box.get("1.0", "end-1c")
    if not entry.strip():
        messagebox.showwarning("Warning", "Diary entry is empty!")
        return
    if not username:
        messagebox.showwarning("Warning", "Please enter your name first.")
        return

    # Set filename based on the date
    filename = f"diary_entries/{username}/{datetime.now().strftime('%Y-%m-%d')}.txt"

    # Get the current timestamp for the entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Append the text to the file with a timestamp
    with open(filename, "a") as file:
        file.write(f"\n\n--- {timestamp} ---\n")
        file.write(entry)

    messagebox.showinfo("Success", "Diary entry saved.")
    update_entry_dates()  # Refresh available entries

# Function to load a diary entry
def load_entry():
    if not username:
        messagebox.showwarning("Warning", "Please enter your name first.")
        return

    selected_date = entry_dates_combobox.get()
    if not selected_date:
        messagebox.showwarning("Warning", "Please select an entry date.")
        return

    filename = f"diary_entries/{username}/{selected_date}.txt"
    
    if os.path.exists(filename):
        with open(filename, "r") as file:
            entry = file.read()
            text_box.delete("1.0", "end")
            text_box.insert("1.0", entry)
        messagebox.showinfo("Success", f"Diary entry loaded from {selected_date}.txt")
    else:
        messagebox.showwarning("Warning", f"No entry found for {selected_date}.")

# Function to clear the text box
def clear_text():
    text_box.delete("1.0", "end")

# Update the available entry dates in the dropdown
def update_entry_dates():
    if not username:
        return
    user_dir = f"diary_entries/{username}"
    if os.path.exists(user_dir):
        dates = [f.replace(".txt", "") for f in os.listdir(user_dir) if f.endswith(".txt")]
        dates.sort(reverse=True)
        entry_dates_combobox['values'] = dates
    else:
        entry_dates_combobox['values'] = []

# Create the main window
root = tk.Tk()
root.title("Personal Diary Application")
root.geometry("500x500")
root.minsize(400, 300)

# Username input
name_label = tk.Label(root, text="Enter your name:")
name_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=10, pady=5)

set_username_button = tk.Button(root, text="Set Username", command=set_username, font=("Arial", 10), bg="#ADD8E6")
set_username_button.grid(row=0, column=2, padx=10, pady=5)

# Button to reset username
new_username_button = tk.Button(root, text="New Username", command=reset_username, font=("Arial", 10), bg="#FFA07A")
new_username_button.grid(row=1, column=2, padx=10, pady=5)

# Username display label
username_label = tk.Label(root, text="", font=("Arial", 12))
username_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Text box for diary entry
text_box = tk.Text(root, wrap="word", font=("Arial", 12), height=15)
text_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Frame for buttons
button_frame = tk.Frame(root)
button_frame.grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")

# Buttons to save, load, and clear diary entry
save_button = tk.Button(button_frame, text="Save Entry", command=save_entry, font=("Arial", 10), bg="#90EE90")
save_button.grid(row=0, column=0, padx=5, sticky="ew")

load_button = tk.Button(button_frame, text="Load Entry", command=load_entry, font=("Arial", 10), bg="#FFD700")
load_button.grid(row=0, column=1, padx=5, sticky="ew")

clear_button = tk.Button(button_frame, text="Clear Text", command=clear_text, font=("Arial", 10), bg="#FF6347")
clear_button.grid(row=0, column=2, padx=5, sticky="ew")

# Dropdown to select date for loading entries
entry_dates_label = tk.Label(root, text="Select Entry Date:")
entry_dates_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

entry_dates_combobox = ttk.Combobox(root, state="readonly", font=("Arial", 10))
entry_dates_combobox.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

# Configure grid for resizing
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

# Start the main loop
root.mainloop()
