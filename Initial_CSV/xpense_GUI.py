#This code uses tkinter for its GUI

import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import pandas as pd

root = tk.Tk()
root.title("Expense Tracker")

income = 0
savings = 0
current = 0
expenses = {}

income_data = "income.csv"
expenses_data = "expenses.csv"
savings_data = "savings.csv"

def income_save():
    with open(income_data, mode='w', newline='') as file: #with open(income_data, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Income"])
        writer.writerow([income])
    print("Income data is saved")

def income_load():
    global income
    if os.path.exists(income_data):   #Check if file exists
        with open(income_data, mode='r') as file:
            reader = csv.reader(file)
            try:
                next(reader)
                for row in reader:
                    income = float(row[0])
            except (StopIteration, IndexError):
                print("Income file is Empty")
    else:
        print(f"Income file '{income_data}' not found")

def add_income():
    global income
    try:
        amount = float(input(income_entry.get()))
        income += amount
        messagebox.showinfo(f"Successfull added income {income}")
        income_entry.delete(0, tk.END)
    except ValueError:
            messagebox.showerror("Invalid Amount", "Kindlt enter a valid amount")
    income += amount
    income_save()


def savings_save():
    with open(savings_data, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Savings"])
        writer.writerow([savings])
    print("Savings data is saved")

def savings_load():
    global savings
    if os.path.exists(savings_data):
        with open(income_data, mode='r') as file:
            reader = csv.reader(file)
            try:
                next(reader) #Pass the header row.
                for row in reader:
                    savings = float(row[0])
            except (StopIteration, IndexError):
                print("Savings File is empty/corrupt")
    else:
        print(f"Savings file '{savings_data}' is not found.")


def add_savings():
    global savings
    try: 
        s_amount = float(input(savings_entry.get()))
        savings += s_amount
        current = income - s_amount
        messagebox.showinfor(f"Successfully added savings {savings}")
        savings_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Kindly enter a valid amount")
    savings_save()
    print("\n")


def expenses_save(category, amount):
    with open(expenses_data, mode='a', newline='') as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        writer.writerow([category, amount, timestamp])
        print("Expenses data is saved")

def expenses_load():
    global expenses
    if os.path.exists(expenses_data):
        expenses_df = pd.read_csv(expenses_data, names=['Category', 'Amount', 'Timestamp'])
        expenses_df['Amount'] = pd.to_numeric(expenses_df['Amount'], errors='coerce')

        for _, row in expenses_df.iterrows():
            category = row['Category'].strip()
            amount = row['Amount']
            if category in expenses:
                expenses[category] += amount
            else:
                expenses[category] = amount

    else:
        print(f"Expense file '{expenses_data}' not found")


def add_expenses():
    global expenses
    category = category_entry.get()
    try:
        amount = float(amount_entry.get())
        if category in expenses:
            expenses[category] += amount
        else:
            expenses[category] = amount
        
        expenses_save(category, amount)
        messagebox.showinfo(f"Successfully added expense {category}: {amount}")
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
    except:
        messagebox.showerror("Invalid Input", "Kindly enter a valid amount.")

    print(f"Expenses added: {category} : {amount}")
    expenses_save(category, amount) #Expenses are saved with their timestamp
    print("\n")


def account_summary():
    total_expenses = sum(expenses.values())
    current = income - total_expenses
    summary = f"Total Income: {income}\n Savings: {savings}\nTotal Expenses: {total_expenses}\nCurrent: {current}"
    messagebox.showinfo("Budget Summary: ", summary)

    print("--- Expenses BreakDown ---")
    for category, amount in expenses.items():
        print(f"{category}: {amount}")
        print("\n")


root = tk.Tk()
root.title("Expense Tracker")

tk.Label(root, text="Income:").grid(row=0, column=0)
income_entry = tk.Entry(root)
income_entry.grid(row=0, column=1)
tk.Button(root, text="Add Income", command=add_income).grid(row=0, column=2)

tk.Label(root, text="Savings:").grid(row=1, column=0)
savings_entry = tk.Entry(root)
savings_entry.grid(row=1, column=1)
tk.Button(root, text="Add Savings", command=add_savings).grid(row=1, column=2)

tk.Label(root, text="Category:").grid(row=2, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=2, column=1)

tk.Label(root, text="Amount:").grid(row=3, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1)
tk.Button(root, text="Add Expense", command=add_expenses).grid(row=4, column=1)

tk.Button(root, text="Display Summary", command=account_summary).grid(row=5, column=1)

root.mainloop()