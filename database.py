# database.py

import sqlite3
from sqlite3 import Error

def create_connection(db_file='expenses.db'):
    """
    Create a database connection to the SQLite database specified by db_file.

    Parameters:
        db_file (str): The filename of the SQLite database.

    Returns:
        Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # Enable foreign key support if needed in future enhancements
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table():
    """
    Create the expenses table in the database if it doesn't already exist.
    """
    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    '''
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
            print("Expenses table is ready.")
        except Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

def add_expense(amount, category, description, date):
    """
    Add a new expense to the expenses table.

    Parameters:
        amount (float): The amount of the expense.
        category (str): The category of the expense.
        description (str): A description of the expense.
        date (str): The date of the expense in YYYY-MM-DD format.

    Returns:
        expense_id (int): The ID of the newly added expense, or None if failed.
    """
    sql = '''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    '''
    conn = create_connection()
    expense_id = None
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (amount, category, description, date))
            conn.commit()
            expense_id = cursor.lastrowid
            print(f"Expense added with ID: {expense_id}")
        except Error as e:
            print(f"Error adding expense: {e}")
        finally:
            conn.close()
    return expense_id

def view_expenses():
    """
    Retrieve all expenses from the expenses table.

    Returns:
        List of tuples containing expense records.
    """
    sql = '''
        SELECT id, amount, category, description, date FROM expenses
        ORDER BY date DESC
    '''
    conn = create_connection()
    expenses = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            expenses = cursor.fetchall()
            print(f"Retrieved {len(expenses)} expenses.")
        except Error as e:
            print(f"Error retrieving expenses: {e}")
        finally:
            conn.close()
    return expenses

def edit_expense(expense_id, amount, category, description, date):
    """
    Update an existing expense in the expenses table.

    Parameters:
        expense_id (int): The ID of the expense to update.
        amount (float): The new amount.
        category (str): The new category.
        description (str): The new description.
        date (str): The new date in YYYY-MM-DD format.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    sql = '''
        UPDATE expenses
        SET amount = ?, category = ?, description = ?, date = ?
        WHERE id = ?
    '''
    conn = create_connection()
    success = False
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (amount, category, description, date, expense_id))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"No expense found with ID: {expense_id}")
            else:
                print(f"Expense with ID: {expense_id} updated successfully.")
                success = True
        except Error as e:
            print(f"Error updating expense: {e}")
        finally:
            conn.close()
    return success

def delete_expense(expense_id):
    """
    Delete an expense from the expenses table.

    Parameters:
        expense_id (int): The ID of the expense to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    sql = '''
        DELETE FROM expenses WHERE id = ?
    '''
    conn = create_connection()
    success = False
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (expense_id,))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"No expense found with ID: {expense_id}")
            else:
                print(f"Expense with ID: {expense_id} deleted successfully.")
                success = True
        except Error as e:
            print(f"Error deleting expense: {e}")
        finally:
            conn.close()
    return success

def generate_report():
    """
    Generate a report summarizing total expenses per category.

    Returns:
        List of tuples containing category and total amount.
    """
    sql = '''
        SELECT category, SUM(amount) as total_amount
        FROM expenses
        GROUP BY category
        ORDER BY total_amount DESC
    '''
    conn = create_connection()
    report = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            report = cursor.fetchall()
            print("Report generated successfully.")
        except Error as e:
            print(f"Error generating report: {e}")
        finally:
            conn.close()
    return report

def initialize_database():
    """
    Initialize the database by creating the expenses table.
    This function can be called when the module is imported to ensure the table exists.
    """
    create_table()

# Initialize the database when the module is imported
initialize_database()

# Optional: Allow running database setup independently
if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
