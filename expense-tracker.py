import argparse
import json
from datetime import datetime

# File to store expenses
EXPENSE_FILE = 'expenses.json'

def load_expenses():
    try:
        with open(EXPENSE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

def add_expense(description, amount):
    expenses = load_expenses()
    expense_id = len(expenses) + 1
    date = datetime.now().strftime('%Y-%m-%d')
    expenses.append({'id': expense_id, 'date': date, 'description': description, 'amount': amount})
    save_expenses(expenses)
    print(f'Expense added successfully (ID: {expense_id})')

def list_expenses():
    expenses = load_expenses()
    print(f'{"ID":<4} {"Date":<12} {"Description":<20} {"Amount":<10}')
    for expense in expenses:
        print(f'{expense["id"]:<4} {expense["date"]:<12} {expense["description"]:<20} {expense["amount"]:<10}')

def delete_expense(expense_id):
    expenses = load_expenses()
    expenses = [expense for expense in expenses if expense['id'] != expense_id]
    save_expenses(expenses)
    print('Expense deleted successfully')

def summary():
    expenses = load_expenses()
    total = sum(expense['amount'] for expense in expenses)
    print(f'Total expenses: ${total}')

def summary_month(month):
    expenses = load_expenses()
    total = sum(expense['amount'] for expense in expenses if datetime.strptime(expense['date'], '%Y-%m-%d').month == month)
    print(f'Total expenses for month {month}: ${total}')

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--description', required=True)
    add_parser.add_argument('--amount', type=float, required=True)

    list_parser = subparsers.add_parser('list')

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('--id', type=int, required=True)

    summary_parser = subparsers.add_parser('summary')
    summary_parser.add_argument('--month', type=int, required=False)

    args = parser.parse_args()

    if args.command == 'add':
        add_expense(args.description, args.amount)
    elif args.command == 'list':
        list_expenses()
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'summary':
        if args.month:
            summary_month(args.month)
        else:
            summary()

if __name__ == '__main__':
    main()
