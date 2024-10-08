# expense_tracker.py
import sqlite3
from tabulate import tabulate
import datetime

def create_connection():
    conn = sqlite3.connect('expenses.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, category, description, date):
    try:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, category, description, date))
        conn.commit()
        conn.close()
        print("Expense added successfully.")
    except Exception as e:
        print(f"Error adding expense: {e}")

def view_expenses():
    try:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses')
        rows = cursor.fetchall()
        conn.close()
        if rows:
            print(tabulate(rows, headers=["ID", "Amount", "Category", "Description", "Date"], tablefmt="pretty"))
        else:
            print("No expenses found.")
    except Exception as e:
        print(f"Error viewing expenses: {e}")

def edit_expense(expense_id, amount, category, description, date):
    try:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE expenses
            SET amount = ?, category = ?, description = ?, date = ?
            WHERE id = ?
        ''', (amount, category, description, date, expense_id))
        if cursor.rowcount == 0:
            print("No expense found with the given ID.")
        else:
            print("Expense updated successfully.")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error editing expense: {e}")

def delete_expense(expense_id):
    try:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        if cursor.rowcount == 0:
            print("No expense found with the given ID.")
        else:
            print("Expense deleted successfully.")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error deleting expense: {e}")

def generate_report():
    try:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        rows = cursor.fetchall()
        conn.close()
        if rows:
            print("Expense Report by Category:")
            print(tabulate(rows, headers=["Category", "Total Amount"], tablefmt="pretty"))
        else:
            print("No expenses to report.")
    except Exception as e:
        print(f"Error generating report: {e}")

def main_menu():
    print("\n===== Expense Tracker =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Edit Expense")
    print("4. Delete Expense")
    print("5. Generate Report")
    print("6. Exit")

def get_date():
    while True:
        date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
        if not date_str:
            return datetime.date.today().isoformat()
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Invalid date format. Please try again.")

def run():
    create_table()
    while True:
        main_menu()
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ")
                description = input("Enter description (optional): ")
                date = get_date()
                add_expense(amount, category, description, date)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == '2':
            view_expenses()
        
        elif choice == '3':
            try:
                expense_id = int(input("Enter the ID of the expense to edit: "))
                amount = float(input("Enter new amount: "))
                category = input("Enter new category: ")
                description = input("Enter new description (optional): ")
                date = get_date()
                edit_expense(expense_id, amount, category, description, date)
            except ValueError:
                print("Invalid input. Please enter correct data types.")
        
        elif choice == '4':
            try:
                expense_id = int(input("Enter the ID of the expense to delete: "))
                delete_expense(expense_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        
        elif choice == '5':
            generate_report()
        
        elif choice == '6':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

if __name__ == "__main__":
    run()
