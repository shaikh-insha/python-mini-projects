# Enhanced ExpenseTracker: Cleaner, More Modular, Robust

import json
import os
from datetime import datetime
import pandas as pd
import sqlite3

try:
    import matplotlib.pyplot as plt  # type: ignore
except ImportError:
    plt = None


class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.predefined_categories = [
            "Groceries", "Transportation", "Utilities", "Entertainment", "Others"
        ]
        self.custom_categories = []
        self.data_file = "expenses.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.expenses = data.get("expenses", [])
                self.custom_categories = data.get("custom_categories", [])

    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump({
                "expenses": self.expenses,
                "custom_categories": self.custom_categories
            }, file, indent=4)

    def get_all_categories(self):
        return self.predefined_categories + self.custom_categories

    def prompt_category(self):
        categories = self.get_all_categories()
        for idx, cat in enumerate(categories, 1):
            print(f"{idx}. {cat}")
        print(f"{len(categories) + 1}. Add a new category")

        try:
            choice = int(input("Enter the number of the category: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            elif choice == len(categories) + 1:
                new_category = input("Enter the new category name: ").strip()
                if new_category and new_category not in self.get_all_categories():
                    self.custom_categories.append(new_category)
                    return new_category
                else:
                    print("Invalid or duplicate category.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
        return None

    def add_expense(self):
        try:
            amount = float(input("Enter the amount spent: "))
            description = input("Enter a brief description: ").strip()
            if not description:
                print("Description cannot be empty.")
                return
            
            category = self.prompt_category()
            if not category:
                return

            expense = {
                "amount": amount,
                "description": description,
                "category": category,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            self.expenses.append(expense)
            self.save_data()
            print("Expense added successfully!")
        except ValueError:
            print("Invalid amount entered.")

    def view_summary_by_category(self):
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        category_totals = {}
        for expense in self.expenses:
            category_totals[expense["category"]] = category_totals.get(expense["category"], 0) + expense["amount"]

        print("\nSpending by Category:")
        for category, amount in category_totals.items():
            print(f"{category}: ${amount:.2f}")

        if plt:
            self.plot_expenses(category_totals)
        else:
            print("Matplotlib not installed. Skipping chart.")

    def plot_expenses(self, category_totals):
        plt.figure(figsize=(8, 6))
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
        plt.title("Expenses by Category")
        plt.show()

    def export_to_excel(self):
        self.export_generic("xlsx", lambda df, path: df.to_excel(path, index=False))

    def export_to_txt(self):
        if not self.expenses:
            print("No expenses to export.")
            return

        path = input("Enter the path for the text file: ")
        with open(path, "w") as file:
            for e in self.expenses:
                file.write(f"Amount: {e['amount']}, Description: {e['description']}, Category: {e['category']}, Date: {e['date']}\n")
        print(f"Exported to {path}")

    def export_to_db(self):
        if not self.expenses:
            print("No expenses to export.")
            return

        db_path = input("Enter SQLite DB path (e.g. expenses.db): ")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        amount REAL, description TEXT, category TEXT, date TEXT)''')
        for e in self.expenses:
            cur.execute("INSERT INTO expenses VALUES (?, ?, ?, ?)",
                        (e["amount"], e["description"], e["category"], e["date"]))
        conn.commit()
        conn.close()
        print(f"Exported to {db_path}")

    def export_generic(self, file_type, export_func):
        if not self.expenses:
            print("No expenses to export.")
            return
        df = pd.DataFrame(self.expenses)
        df.columns = ["Amount", "Description", "Category", "Date"]
        path = input(f"Enter output {file_type.upper()} file path: ")
        export_func(df, path)
        print(f"Exported to {path}")

    def manage_categories(self):
        print("\nCategory Management")
        print("1. Add", "2. Edit", "3. Remove", "4. View")
        choice = input("Choose an option: ")

        actions = {
            "1": self.add_custom_category,
            "2": self.edit_custom_category,
            "3": self.remove_custom_category,
            "4": self.view_all_categories
        }
        actions.get(choice, lambda: print("Invalid choice."))()

    def add_custom_category(self):
        new_cat = input("Enter new category name: ").strip()
        if new_cat and new_cat not in self.get_all_categories():
            self.custom_categories.append(new_cat)
            self.save_data()
            print(f"Category '{new_cat}' added.")
        else:
            print("Invalid or duplicate category.")

    def edit_custom_category(self):
        if not self.custom_categories:
            print("No custom categories available.")
            return
        for idx, cat in enumerate(self.custom_categories, 1):
            print(f"{idx}. {cat}")
        try:
            choice = int(input("Enter category number to rename: "))
            if 1 <= choice <= len(self.custom_categories):
                new_name = input("New name: ").strip()
                if new_name:
                    self.custom_categories[choice - 1] = new_name
                    self.save_data()
                    print("Category renamed.")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input.")

    def remove_custom_category(self):
        if not self.custom_categories:
            print("No custom categories available.")
            return
        for idx, cat in enumerate(self.custom_categories, 1):
            print(f"{idx}. {cat}")
        try:
            choice = int(input("Enter category number to remove: "))
            if 1 <= choice <= len(self.custom_categories):
                removed = self.custom_categories.pop(choice - 1)
                self.save_data()
                print(f"Category '{removed}' removed.")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input.")

    def view_all_categories(self):
        print("\nPredefined:", *self.predefined_categories, sep="\n- ")
        print("\nCustom:", *self.custom_categories if self.custom_categories else ["(None)"], sep="\n- ")

    def main_menu(self):
        while True:
            print("\nExpense Tracker")
            print("1. Add Expense")
            print("2. View Summary")
            print("3. Export")
            print("4. Manage Categories")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_summary_by_category()
            elif choice == "3":
                self.export_menu()
            elif choice == "4":
                self.manage_categories()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

    def export_menu(self):
        print("\nExport Options")
        print("1. Excel", "2. Text", "3. SQLite DB")
        choice = input("Choose an option: ")
        {
            "1": self.export_to_excel,
            "2": self.export_to_txt,
            "3": self.export_to_db
        }.get(choice, lambda: print("Invalid choice."))()


if __name__ == "__main__":
    ExpenseTracker().main_menu()
