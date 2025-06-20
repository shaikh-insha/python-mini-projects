import json
import os
from datetime import datetime
import pandas as pd

try:
    import matplotlib.pyplot as plt  # type: ignore
except ImportError:
    plt = None


class PersonalExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.predefined_categories = ["Groceries", "Transportation", "Utilities", "Entertainment", "Others"]
        self.custom_categories = []
        self.data_file = "expenses.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.expenses = data.get("expenses", [])
                self.custom_categories = data.get("custom_categories", [])

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump({
                "expenses": self.expenses,
                "custom_categories": self.custom_categories
            }, f, indent=4)

    def get_all_categories(self):
        return self.predefined_categories + self.custom_categories

    def add_expense(self):
        try:
            amount = float(input("💰 Enter amount spent: "))
            description = input("📝 Description: ").strip()
            if not description:
                print("❌ Description cannot be empty.")
                return

            categories = self.get_all_categories()
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            print(f"{len(categories) + 1}. ➕ Add new category")

            choice = int(input("Select category number: "))
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
            elif choice == len(categories) + 1:
                category = input("Enter new category name: ").strip()
                if not category or category in categories:
                    print("❌ Invalid or duplicate category.")
                    return
                self.custom_categories.append(category)
            else:
                print("❌ Invalid category choice.")
                return

            self.expenses.append({
                "amount": amount,
                "description": description,
                "category": category,
                "date": datetime.now().strftime("%Y-%m-%d")
            })
            self.save_data()
            print("✅ Expense added!")
        except ValueError:
            print("❌ Invalid amount. Please enter a number.")

    def view_summary(self):
        if not self.expenses:
            print("📭 No expenses recorded.")
            return

        totals = {}
        for e in self.expenses:
            totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]

        print("\n📊 Expense Summary by Category:")
        for cat, amt in totals.items():
            print(f"• {cat}: ₹{amt:.2f}")

        if totals:
            max_cat = max(totals, key=totals.get)
            min_cat = min(totals, key=totals.get)
            print(f"\n🔺 Highest: {max_cat} – ₹{totals[max_cat]:.2f}")
            print(f"🔻 Lowest: {min_cat} – ₹{totals[min_cat]:.2f}")

        if plt:
            self.plot_chart(totals)
        else:
            print("📉 Matplotlib not available – skipping chart.")

    def plot_chart(self, totals):
        plt.figure(figsize=(7, 6))
        plt.pie(totals.values(), labels=totals.keys(), autopct='%1.1f%%')
        plt.title("Expenses by Category")
        plt.show()

    def manage_categories(self):
        print("\n⚙️ Category Manager")
        print("1. ➕ Add Custom Category")
        print("2. ✏️ Edit Custom Category")
        print("3. ❌ Remove Custom Category")
        print("4. 📋 View All Categories")
        choice = input("Choose option: ")

        {
            "1": self.add_custom_category,
            "2": self.edit_custom_category,
            "3": self.remove_custom_category,
            "4": self.view_categories
        }.get(choice, lambda: print("❌ Invalid choice."))()

    def add_custom_category(self):
        name = input("Enter new category name: ").strip()
        if name and name not in self.get_all_categories():
            self.custom_categories.append(name)
            self.save_data()
            print(f"✅ Category '{name}' added.")
        else:
            print("❌ Invalid or duplicate category.")

    def edit_custom_category(self):
        if not self.custom_categories:
            print("📭 No custom categories.")
            return

        for i, cat in enumerate(self.custom_categories, 1):
            print(f"{i}. {cat}")
        try:
            choice = int(input("Select category to rename: "))
            if 1 <= choice <= len(self.custom_categories):
                new_name = input("New name: ").strip()
                if new_name:
                    self.custom_categories[choice - 1] = new_name
                    self.save_data()
                    print("✅ Category updated.")
                else:
                    print("❌ Empty name.")
        except ValueError:
            print("❌ Invalid input.")

    def remove_custom_category(self):
        if not self.custom_categories:
            print("📭 No custom categories.")
            return

        for i, cat in enumerate(self.custom_categories, 1):
            print(f"{i}. {cat}")
        try:
            choice = int(input("Select category to remove: "))
            if 1 <= choice <= len(self.custom_categories):
                removed = self.custom_categories.pop(choice - 1)
                self.save_data()
                print(f"✅ Removed: {removed}")
            else:
                print("❌ Invalid number.")
        except ValueError:
            print("❌ Invalid input.")

    def view_categories(self):
        print("\n📦 Predefined:")
        for c in self.predefined_categories:
            print(f"• {c}")
        print("\n🛠️ Custom:")
        if self.custom_categories:
            for c in self.custom_categories:
                print(f"• {c}")
        else:
            print("• (None)")

    def main_menu(self):
        while True:
            print("\n🧾 Personal Expense Tracker")
            print("1. ➕ Add Expense")
            print("2. 📊 View Summary")
            print("3. ⚙️ Manage Categories")
            print("4. 🚪 Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_summary()
            elif choice == "3":
                self.manage_categories()
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice.")


if __name__ == "__main__":
    tracker = PersonalExpenseTracker()
    tracker.main_menu()
