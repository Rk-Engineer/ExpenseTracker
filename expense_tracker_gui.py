# expense_tracker_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import (
    add_expense,
    view_expenses,
    edit_expense,
    delete_expense,
    generate_report
)

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Add Expense Frame
        self.add_expense_frame = tk.LabelFrame(self.root, text="Add New Expense", padx=10, pady=10)
        self.add_expense_frame.pack(fill="x", padx=20, pady=10)

        # Amount
        tk.Label(self.add_expense_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = tk.Entry(self.add_expense_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Category
        tk.Label(self.add_expense_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(
            self.add_expense_frame,
            textvariable=self.category_var,
            state="readonly",
            values=["Food", "Transport", "Entertainment", "Utilities", "Others"]
        )
        self.category_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.category_combobox.current(0)  # Set default value

        # Description
        tk.Label(self.add_expense_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.description_entry = tk.Entry(self.add_expense_frame, width=50)
        self.description_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # Date
        tk.Label(self.add_expense_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = tk.Entry(self.add_expense_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default to today

        # Add Button
        self.add_button = tk.Button(self.add_expense_frame, text="Add Expense", command=self.add_expense_gui)
        self.add_button.grid(row=2, column=3, padx=5, pady=5, sticky="e")

        # Expenses Display Frame
        self.expenses_frame = tk.LabelFrame(self.root, text="Expenses", padx=10, pady=10)
        self.expenses_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview for Expenses
        columns = ("ID", "Amount", "Category", "Description", "Date")
        self.expenses_tree = ttk.Treeview(self.expenses_frame, columns=columns, show="headings")
        for col in columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, anchor="center")
        self.expenses_tree.pack(fill="both", expand=True)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.expenses_frame)
        self.buttons_frame.pack(pady=10)

        self.edit_button = tk.Button(self.buttons_frame, text="Edit Selected", command=self.edit_expense_gui)
        self.edit_button.grid(row=0, column=0, padx=10)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete Selected", command=self.delete_expense_gui)
        self.delete_button.grid(row=0, column=1, padx=10)

        self.refresh_button = tk.Button(self.buttons_frame, text="Refresh", command=self.refresh_expenses)
        self.refresh_button.grid(row=0, column=2, padx=10)

        # Report Button
        self.report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report_gui)
        self.report_button.pack(pady=10)

        # Load expenses initially
        self.refresh_expenses()

    def add_expense_gui(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            description = self.description_entry.get()
            date_str = self.date_entry.get()

            # Validate date format
            datetime.strptime(date_str, '%Y-%m-%d')

            add_expense(amount, category, description, date_str)
            messagebox.showinfo("Success", "Expense added successfully.")
            self.refresh_expenses()

            # Clear input fields
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def refresh_expenses(self):
        # Clear the current contents
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)

        # Fetch data from the database
        expenses = view_expenses()
        for expense in expenses:
            self.expenses_tree.insert("", tk.END, values=expense)

    def edit_expense_gui(self):
        selected_item = self.expenses_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to edit.")
            return

        expense = self.expenses_tree.item(selected_item)["values"]
        self.open_edit_window(expense)

    def open_edit_window(self, expense):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Expense")
        edit_window.geometry("400x300")

        tk.Label(edit_window, text="Amount:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        amount_entry = tk.Entry(edit_window)
        amount_entry.grid(row=0, column=1, padx=10, pady=10)
        amount_entry.insert(0, expense[1])

        tk.Label(edit_window, text="Category:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(
            edit_window,
            textvariable=category_var,
            state="readonly",
            values=["Food", "Transport", "Entertainment", "Utilities", "Others"]
        )
        category_combobox.grid(row=1, column=1, padx=10, pady=10)
        category_combobox.set(expense[2])

        tk.Label(edit_window, text="Description:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        description_entry = tk.Entry(edit_window, width=30)
        description_entry.grid(row=2, column=1, padx=10, pady=10)
        description_entry.insert(0, expense[3])

        tk.Label(edit_window, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        date_entry = tk.Entry(edit_window)
        date_entry.grid(row=3, column=1, padx=10, pady=10)
        date_entry.insert(0, expense[4])

        def save_changes():
            try:
                amount = float(amount_entry.get())
                category = category_var.get()
                description = description_entry.get()
                date_str = date_entry.get()

                # Validate date format
                datetime.strptime(date_str, '%Y-%m-%d')

                edit_expense(expense[0], amount, category, description, date_str)
                messagebox.showinfo("Success", "Expense updated successfully.")
                edit_window.destroy()
                self.refresh_expenses()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid data.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=20)

    def delete_expense_gui(self):
        selected_item = self.expenses_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to delete.")
            return

        expense = self.expenses_tree.item(selected_item)["values"]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete expense ID {expense[0]}?")
        if confirm:
            try:
                delete_expense(expense[0])
                messagebox.showinfo("Success", "Expense deleted successfully.")
                self.refresh_expenses()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_report_gui(self):
        report = generate_report()
        if not report:
            messagebox.showinfo("Report", "No expenses to report.")
            return

        report_window = tk.Toplevel(self.root)
        report_window.title("Expense Report")
        report_window.geometry("400x300")

        tk.Label(report_window, text="Expense Report by Category", font=("Arial", 14)).pack(pady=10)

        # Treeview for Report
        columns = ("Category", "Total Amount")
        report_tree = ttk.Treeview(report_window, columns=columns, show="headings")
        for col in columns:
            report_tree.heading(col, text=col)
            report_tree.column(col, anchor="center")
        report_tree.pack(fill="both", expand=True, padx=10, pady=10)

        for row in report:
            report_tree.insert("", tk.END, values=row)

        # Close Button
        close_button = tk.Button(report_window, text="Close", command=report_window.destroy)
        close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
