import csv
import os
from pathlib import Path
from datetime import datetime
from secrets import choice

expenses = []
budgets = {}
ignored_budget_months = set()

DATA_FOLDER = Path("/Users/simranchhetry/Documents/Gen AI and Machine Learning/Python Projects/Expense Tracker")

DATA_FOLDER.mkdir(parents=True, exist_ok=True)

FILENAME = DATA_FOLDER / "expenses.csv"
BUDGET_FILE = DATA_FOLDER / "budgets.csv"

print(f"\nExpense data will be stored at:\n{FILENAME}\n")



# 1. Add expense: 
def add_expense():
    from datetime import datetime, date

    categories = [
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Healthcare",
        "Outings",
        "Other"
    ]

    print("\n==================== Add Expense ====================\n")
    print("Enter the details below to record a new expense.\n")

    # Date
    while True:
        try:
            expense_date = datetime.strptime(
                input("Enter date (YYYY-MM-DD): ").strip(),
                "%Y-%m-%d"
            ).date()

            if expense_date > date.today():
                print("The date cannot be in the future.\n")
                continue

            break

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.\n")

    year = expense_date.year
    month = expense_date.month

    if (
        (year, month) not in budgets
        and (year, month) not in ignored_budget_months
    ):

        print(f"\nNo budget has been set for {month:02d}/{year}.")

        while True:
            reply = input(
                "Would you like to set one now? (Y/N): "
            ).strip().upper()

            if reply == "Y":
                set_budget(year, month)
                break

            elif reply == "N":
                ignored_budget_months.add((year, month))
                print("Continuing without a budget.\n")
                break

            else:
                print("Please enter Y or N.")

    # Category
    while True:
        print("\nExpense Categories")
        print("-" * 25)

        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")

        category_choice = input("\nChoose a category (1-8): ").strip()

        if category_choice.isdigit():
            category_choice = int(category_choice)

            if 1 <= category_choice <= len(categories):
                category = categories[category_choice - 1]
                break

        print("Please enter a number between 1 and 8.\n")

    # Amount
    while True:
        try:
            amount = float(input("\nEnter amount spent (₹): ").strip())

            if amount <= 0:
                print("Amount must be greater than ₹0.\n")
                continue

            break

        except ValueError:
            print("Please enter a valid numeric amount.\n")

    # Description
    while True:
        description = input("\nEnter a brief description: ").strip()

        if description:
            break

        print("Description cannot be empty.\n")

    # Save expense
    expense = {
        "date": expense_date,
        "category": category,
        "amount": amount,
        "description": description
    }

    expenses.append(expense)
    expenses.sort(key=lambda exp: exp["date"])
    print("\n✓ Expense added successfully!\n")




# 2. View expenses
def view_expenses():
    if not expenses:
        print("\nNo expenses have been recorded yet.")
        return

    print("\n==================== Expense History ====================\n")

    print(f"{'No.':<5}{'Date':<15}{'Category':<20}{'Amount':<12}{'Description'}")
    print("-" * 70)

    for i, exp in enumerate(expenses, start=1):
        print(
            f"{i:<5}"
            f"{exp['date'].strftime('%Y-%m-%d'):<15}"
            f"{exp['category']:<20}"
            f"₹{exp['amount']:<11.2f}"
            f"{exp['description']}"
        )

    print("-" * 70)
    print(f"Total expenses recorded: {len(expenses)}\n")




# 3. Set and Track Budget
def set_budget(year=None, month=None):
    print("\n==================== Set Monthly Budget ====================\n")

    # Ask for month and year only if they were not supplied
    if year is None or month is None:
        while True:
            try:
                year = int(input("Enter year (e.g. 2026): "))
                month = int(input("Enter month (1-12): "))

                if month < 1 or month > 12:
                    print("Month must be between 1 and 12.\n")
                    continue

                break

            except ValueError:
                print("Please enter valid numbers.\n")

    while True:
        try:
            budget = float(input("Enter budget (₹): "))

            if budget <= 0:
                print("Budget must be greater than zero.\n")
                continue

            budgets[(year, month)] = budget
            ignored_budget_months.discard((year, month))

            print(
                f"\nBudget for {month:02d}/{year} "
                f"set to ₹{budget:,.2f}\n"
            )
            break

        except ValueError:
            print("Please enter a valid budget amount.\n")

def track_budget():
    print("\n==================== Track Monthly Budget ====================\n")

    try:
        year = int(input("Enter year (e.g. 2026): "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("Month must be between 1 and 12.")
            return

    except ValueError:
        print("Please enter valid numbers.")
        return

    if (year, month) not in budgets:
        print(f"\nNo budget has been set for {month:02d}/{year}.")
        print("Please set a budget first.\n")
        return

    budget = budgets[(year, month)]

    total_spent = sum(
        exp["amount"]
        for exp in expenses
        if exp["date"].year == year and exp["date"].month == month
    )

    remaining = budget - total_spent

    print("\n==================== Budget Summary ====================\n")

    print(f"Month                 : {month:02d}/{year}")
    print(f"Budget                : ₹{budget:,.2f}")
    print(f"Total Spent           : ₹{total_spent:,.2f}")

    if remaining >= 0:
        print(f"Remaining Budget      : ₹{remaining:,.2f}")
        print("\n✓ You are within your monthly budget.")
    else:
        print(f"Amount Over Budget    : ₹{abs(remaining):,.2f}")
        print("\n⚠️ You have exceeded your monthly budget!")




# 4. Save and load expenses as well as budgets
def save_expenses():
    with open(FILENAME, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["date", "category", "amount", "description"])

        for exp in expenses:
            writer.writerow([
                exp["date"].strftime("%Y-%m-%d"),
                exp["category"],
                exp["amount"],
                exp["description"]
            ])

    print(f"\n✓ Expenses successfully saved to:\n{FILENAME}\n")

def save_budgets():
    with open(BUDGET_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["year", "month", "budget"])

        for (year, month), budget in budgets.items():
            writer.writerow([year, month, budget])

    print(f"✓ Budgets successfully saved to:\n{BUDGET_FILE}\n")


def load_expenses():
    if not FILENAME.exists():
        print("No previous expense records found. Starting with an empty tracker.\n")
        return

    expenses.clear()

    with open(FILENAME, mode="r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                expenses.append({
                    "date": datetime.strptime(
                        row["date"], "%Y-%m-%d"
                    ).date(),
                    "category": row["category"],
                    "amount": float(row["amount"]),
                    "description": row["description"]
                })

            except (ValueError, KeyError):
                print(f"Skipped an invalid record: {row}")

    print(f"✓ Loaded {len(expenses)} expense(s) from '{FILENAME.name}'.\n")

def load_budgets():
    if not BUDGET_FILE.exists():
        print("No previous budget records found.\n")
        return

    budgets.clear()

    with open(BUDGET_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                year = int(row["year"])
                month = int(row["month"])
                budget = float(row["budget"])

                budgets[(year, month)] = budget

            except (ValueError, KeyError):
                print(f"Skipped an invalid budget record: {row}")

    print(f"✓ Loaded {len(budgets)} budget(s).\n")



# 5. Interactive menu
def show_menu():
    print("\n==================================================")
    print("           Personal Expense Tracker")
    print("==================================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Set Monthly Budget")
    print("4. Track Budget")
    print("5. Save Data")
    print("6. Exit")
    print("==================================================")


def main():
    load_expenses()
    load_budgets()

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            set_budget()

        elif choice == "4":
            track_budget()

        elif choice == "5":
            save_expenses()
            save_budgets()

        elif choice == "6":
            save_expenses()  
            save_budgets()
            print("\nThank you for using the Personal Expense Tracker!")
            print("Your expenses have been saved successfully.")
            print("Goodbye!\n")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.\n")


if __name__ == "__main__":
    main()