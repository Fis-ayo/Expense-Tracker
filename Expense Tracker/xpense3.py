#This is designed to implement the use of SQLlite to increase code optimization and use of IDs for easy implentation
# I decided to use SQL because comapared to CSV I don't have to create files for each user.

from datetime import datetime
import sqlite3
import bcrypt

#Creating db tables to store all user's data


def user_table():
    connector = sqlite3.connect('expense_database.db')
    cursor = connector.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   username TEXT NOT NULL UNIQUE,
                   password_hash TEXT NOT NULL,
                   name TEXT,
                   email TEXT NOT NULL UNIQUE,
                   phone_no TEXT,
                   address TEXT) ''')
    
    cursor.execute(''' CREATE TABLE IF NOT EXISTS income(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   userId INTEGER,
                   amount REAL,
                   timestamp DATETIME DEFUALT CURRENT_TIMESTAMP,
                   FOREIGN KEY(userId) REFERENCES users(id))''')
    
    cursor.execute(''' CREATE TABLE IF NOT EXISTS savings(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   userId INTEGER,
                   amount REAL,
                   timestamp DATETIME DEFUALT CURRENT_TIMESTAMP,
                   FOREIGN KEY(userId) REFERENCES users(id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   userId INTEGER,
                   category TEXT,
                   amount REAL,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(userId) REFERENCES users(id))''')
    
    connector.commit()
    connector.close()

user_table()

def user_registration():

    #Code to collect user data upon registration.
    name = input("NAME: ")
    email = input("EMAIL: ")
    phone_no = input("PHONE NUMBER: ")
    address = input("ADDRESS: ")
    username = input("USERNAME: ")
    password = input("PASSWORD: ")


    #Hashing password for east comparison later
    password_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())  #Converted the password to bytes and generated a salt(Ensures identical passwords have diff. hashes).

    #Store User Data in created database
    connector = sqlite3.connect('expense_database.db')
    cursor = connector.cursor()

    try:
        cursor.execute (''' INSERT INTO users
                        (name, email, phone_no, address, username, password_hash)
                        VALUES (?, ?, ?, ?, ?, ?)''', (name, email, phone_no, address, username, password_hash))
        
        connector.commit()
        print(f"{name}, Welcome to Expense Tracker")
    
    except sqlite3.IntegrityError:
        print("Username or email already exists!")
    
    finally:
        connector.close()


#This function to make sure users don't have to register everytime
def user_login():
    username = input("USERNAME: ")
    password = input("PASSWORD: ")

    connector = sqlite3.connect("expense_database.db")
    cursor = connector.cursor()

    cursor.execute('''SELECT password_hash FROM users WHERE username=?''', (username,))
    res = cursor.fetchone()

    if res:
        password_hash = res[0]
        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            print(f"Welcome {username}!")
            cursor.execute('''SELECT id FROM users WHERE username = ?''', (username,))
            userId = cursor.fetchone()[0]
            connector.close()
            return userId
        else:
            print("Incorrect Password!")
            return None

    else:
        print("Username does not exist")
        return None
    
  


#-------------Income Operations-------------


def add_income(userId):
    try: 
        connector = sqlite3.connect('expense_database.db')
        cursor = connector.cursor()


        new_income = float(input("INCOME: $"))

        #Fetch existing data
        cursor.execute('''SELECT amount FROM income WHERE userId=?''', (userId,))
        res = cursor.fetchone()

        if res:
            exIncome = res[0]
            total_income = exIncome + new_income
            cursor.execute('''UPDATE income SET amount = ? WHERE userId = ?''', (total_income, userId))
            print(f"Updated! ${total_income} is in your account")

        else:
            cursor.execute('''INSERT INTO income (userId, amount) VALUES (?, ?)''', (userId, new_income))
            print(f"Added ${new_income}")

        connector.commit()
    except ValueError:
        print("Invalid!")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        connector.close()
    
    

#------------Savings Operations----------------


def add_savings(userId):
    try:
        connector = sqlite3.connect('expense_database.db')
        cursor = connector.cursor()

        saving_option = input("Do you want to add savings in 1. amount or 2. percentage: ")
        if saving_option == "1":
            new_savings = float(input("SAVINGS: $"))     
        elif saving_option == "2":
            percentage = int(input("Percentage of income/100: "))
            cursor.execute('''SELECT amount FROM income WHERE userId = ?''', (userId,))
            amount = cursor.fetchone()[0] or 0.0
            new_savings = amount * (percentage/100) 
        else:
            print("Error try again!")

        #Update Income also
        cursor.execute('''SELECT amount FROM income WHERE userId = ?''', (userId,))
        amount = cursor.fetchone()[0] or 0.0
        total_income = amount - new_savings
        cursor.execute('''UPDATE income SET amount = ? WHERE userId = ?''', (total_income, userId))
    
        #Fetch savings amount if it alread existed
        cursor.execute('''SELECT amount FROM savings WHERE userId = ?''', (userId,))
        res = cursor.fetchone()

        if res:
            ex_savings = res[0]
            total_savings = ex_savings + new_savings
            cursor.execute('''UPDATE savings SET amount = ? WHERE userId = ?''', (total_savings, userId))
            print(f"${total_savings} is savings balance")
        else:
            cursor.execute('''INSERT INTO savings(userId, amount) VALUES(?, ?)''', (userId, new_savings))
            print(f"Added ${new_savings} to savings") 
    
        connector.commit()
    except ValueError:
        print("Invalid!")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        connector.close()
    
    
    print("\n")



#-----------Expenses Operations------------



def add_expenses(userId):
    connector = sqlite3.connect('expense_database.db')
    cursor = connector.cursor()

    cursor.execute('''SELECT amount FROM income WHERE userId=?''', (userId,))
    amount = cursor.fetchone()
    if amount[0] == 0: return

    else: 
        category = input("CATEGORY (e.g Entertainment, Rent, Food): ")
        new_expense = float(input("EXPENSE: $"))

        #Fetch expenses that already existed for the category
        cursor.execute('''SELECT amount FROM expenses WHERE userId = ? AND category = ?''', (userId, category))
        res = cursor.fetchone()

        if res:
            X_expense = res[0]
            total_expense = new_expense + X_expense
            cursor.execute('''UPDATE expenses SET amount = ? WHERE userId = ? AND category = ?''', (total_expense, userId, category))
            print(f"${category} expense is updated!")

        else:
            cursor.execute('''INSERT INTO expenses(userId, category, amount) VALUES(?, ?, ?)''', (userId, category, new_expense))
            print(f"${new_expense} on ${category} is added")

        connector.commit()
        connector.close()
    
    print("\n")




#Display All Accounts


def account_summary(userId):
    connector = sqlite3.connect('expense_database.db')
    cursor = connector.cursor()

    #Program to fetch user total income
    cursor.execute('''SELECT amount FROM income WHERE userId=?''', (userId,))
    res = cursor.fetchone()
    if res: income = res[0]
    else: income = 0.0

    #Program to fetch user total savings
    cursor.execute('''SELECT amount FROM savings WHERE userId=?''', (userId,))
    res = cursor.fetchone()
    if res: savings = res[0]
    else: savings = 0.0

    #Program to fetch user's total expense
    cursor.execute('''SELECT SUM(amount) FROM expenses WHERE userId = ?''', (userId,))
    res = cursor.fetchone()
    total_expenses = res[0] if res[0] is not None else 0
    current = income - total_expenses

    print("\n------ Finance Summary ------")
    print(f"Total Income: ${income}")
    print(f"Savings: ${savings}")
    print(f"Total Expenses: ${total_expenses}\n")
    print(f"Current: ${current}\n")
    

    print("--- Expenses BreakDown ---")

    cursor.execute('''SELECT category, amount FROM expenses WHERE userId=?''', (userId,))
    res = cursor.fetchall()

    if not res:
        print("No available expense")

    else:
        for category, amount in res:
            print(f"{category} : ${amount}\n")


    connector.close()


#-------Loop for user interaction---------


def main_menu():
    userId = None

    while not userId:
        print("1. Register", " 2. Login", " 3. Exit")
        
        login_status = input("OPTION: ")

        if login_status == "1":
            user_registration()
            userId = user_login()
        elif login_status == "2":
            userId = user_login() #If successful, userId = True
            # print(f"userId: {userId}")
        elif login_status == "3":
            print("Thank you for visiting")
            return #Exits
        else:
            print("Invalid Option. Try again!")

    while True:

        print("---------------Expense Tracker----------\n")   

        print("1. Add Income")
        print("2. Create Expense")
        print("3. Add Savings")
        print("4. View Account Summary")
        print("5. Logout")

        
        pick = input("OPTION: ")

        if pick == "1":
            add_income(userId)
        elif pick == "2":
            add_expenses(userId)
        elif pick == "3":
            add_savings(userId)
        elif pick == "4":
            account_summary(userId)
        elif pick == "5":
            userId = None
            print("Logged out!")
            break
        else:                          
            print("Invalid option, please try again!")
    main_menu()



print("---------------Welcome to Expense Tracker----------\n")


main_menu()
