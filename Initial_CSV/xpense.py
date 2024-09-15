import csv
import os
from datetime import datetime




income = 0
savings = 0
current = 0
expenses = {}

income_data = r"C:\Users\USER\Documents\Internship\Expense Tracker\CSV\income.csv"
expenses_data = r"C:\Users\USER\Documents\Internship\Expense Tracker\CSV\expenses.csv"
savings_data = r"C:\Users\USER\Documents\Internship\Expense Tracker\CSV\savings.csv"


#-------------Income Operations-------------


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
    while True:
        try:
            amount = float(input("Enter your income: "))
            break
        except ValueError:
            print("Invalid Amount")
    income += amount
    print("Your ", f" income is updated: {income}")
    income_save()
    print("\n")

    

#------------Savings Operations----------------


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
    saving_prompt = input("Do you want to add in 1. amount or 2. percentage: ")
    if saving_prompt == "1":
        s_amount = float(input("Input amount: "))
        savings += s_amount
        current = income - s_amount
            
    elif saving_prompt == "2":
        s_percentage = int(input("Input percentage of income/100: "))
        savings += (income * (s_percentage/100))
        current = income - (income * (s_percentage/100))
    
    else:
        print("Error try again!")
    
    print(f"Savings is updated: {savings}")
    savings_save()
    print("\n")



#-----------Expenses Operations------------


def expenses_save(category, amount):
    with open(expenses_data, mode='a', newline='') as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        writer.writerow([category, amount, timestamp])
        print("Expenses data is saved")



def expenses_load():
    global expenses
    if os.path.exists(expenses_data):
        with open(expenses_data, mode='r') as file:
            reader = csv.reader(file)
            try:
                next(reader)
                for row in reader:
                    if len(row) == 3:
                        category = row[0].strip()
                        amount = float(row[1].strip()) #Timestamp in row[2], but not used here

                        if category in expenses:
                            expenses[category] += amount
                        else:
                            expenses[category] = amount
            except(StopIteration, IndexError, ValueError):
                print("Expense file is empty")
    else:
        print(f"Expense file '{expenses_data}' not found")

def add_expenses():
    global expenses
    category = input("Enter expense category (e.g Entertainment, Rent, Food): ")
    amount = float(input(f"Enter spent on {category}: "))

    if category in expenses:
        expenses[category] += amount
    else:
        expenses[category] = amount

    print(f"Expenses added: {category} : {amount}")
    expenses_save(category, amount) #Expenses are saved with their timestamp
    print("\n")




#Display All Accounts


def account_summary():
    total_expenses = sum(expenses.values())
    current = income - total_expenses
    print("\n------ Finance Summary ------")
    print(f"Total Income: {income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Current: {current}")
    print(f"Savings: {savings}\n")

    print("--- Expenses BreakDown ---")
    for category, amount in expenses.items():
        print(f"{category}: {amount}")
        print("\n")


#-------Loop for user interaction---------


income_load()
expenses_load()
savings_load()

while True:
    print("---------------Welcome to Expense Tracker----------\n")   

    print("1. Add Income")
    print("2. Create Expense")
    print("3. Add Savings")
    print("4. View Account Summary")
    print("5. Exit")

    print("-----Welcome to Expense Tracker----\n")
    pick = input("What would you like to do today? ")

    if pick == "1":
        add_income()
    elif pick == "2":
        add_expenses()
    elif pick == "3":
        add_savings()
    elif pick == "4":
        account_summary()
    elif pick == "5":
        print("Exiting Expense Tracker. Thank you")
        break
    else:
        print("Invalid option, please try again!")



