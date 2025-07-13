import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

DATABASE_NAME = "expense_tracker.db"
is_logged_in = False

def add_user_to_database(username, password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def user_login():
    attempts_left = 3
    while attempts_left > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            print("Login successful!")
            return username
        else:
            print("Invalid credentials. Please try again.")
            attempts_left -= 1
            if attempts_left > 0:
                print("Attempts left:", attempts_left)
            else:
                print("Too many invalid attempts. Exiting.")
                return None

def delete_user_from_database(username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    
    if user_data:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        cursor.execute("DELETE FROM expenses WHERE username = ?", (username,))
        print("User deleted successfully.")
    else:
        print("User not found.")
    
    conn.commit()
    conn.close()

def add_expense_to_database(username, date, category, amount, paid_by, comments):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO expenses (username, date, category, amount, paid_by, comments)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (username, date, category, amount, paid_by, comments),
    )
    conn.commit()
    conn.close()

def view_expenses_from_database(username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE username = ?", (username,))
    expenses_data = cursor.fetchall()
    conn.close()
    
    if expenses_data:
        expenses_df = pd.DataFrame(
            expenses_data,
            columns=["username", "date", "category", "amount", "paid_by", "comments"],
        )
        print("\nExpense Data:")
        print(expenses_df)
    else:
        print("No expenses found for the user.")

def analyze_expenses_from_database(username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE username = ? GROUP BY category", (username,))
    category_sum = cursor.fetchall()
    conn.close()
    
    if category_sum:
        print("\nExpense Distribution by Category:")
        for category, amount in category_sum:
            print(f"{category}: {amount}")
        
        amounts = [amount for _, amount in category_sum]
        average_amount = np.mean(amounts)
        total_amount = np.sum(amounts)
        max_category_index = np.argmax(amounts)
        max_category = category_sum[max_category_index][0]
        
        categories, amounts = zip(*category_sum)
        plt.bar(categories, amounts)
        plt.title("Expense Distribution by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.show()
        
        print("\nAverage Amount:", average_amount)
        print("Total Amount:", total_amount)
        print("Category with Maximum Spending:", max_category)
    else:
        print("No expenses found for the user.")

def main():
    global is_logged_in
    username = None
    
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add User")
        print("2. Login")
        print("3. Delete User")
        print("4. Add Expense")
        print("5. View Expenses")
        print("6. Analyze Expenses")
        print("7. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            add_user_to_database(username, password)
            print("User created successfully!")
        elif choice == "2":
            username = user_login()
            if username:
                print("Welcome, " + username + "!")
                is_logged_in = True
        elif choice == "3":
            username = input("Enter the username you want to delete: ")
            delete_user_from_database(username)
        elif choice == "4":
            if not is_logged_in:
                print("Please log in first.")
            else:
                date = input("Enter the date (YYYY-MM-DD): ")
                category = input("Enter the category: ")
                amount = float(input("Enter the amount: "))
                paid_by = input("Enter the person who paid: ")
                comments = input("Enter any comments (optional): ")
                add_expense_to_database(username, date, category, amount, paid_by, comments)
        elif choice == "5":
            if not is_logged_in:
                print("Please log in first.")
            else:
                view_expenses_from_database(username)
        elif choice == "6":
            if not is_logged_in:
                print("Please log in first.")
            else:
                analyze_expenses_from_database(username)
        elif choice == "7":
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
