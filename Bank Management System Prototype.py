import tkinter as tk
from tkinter import messagebox, Toplevel
import os

class BankSystem:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.account_file = os.path.join(data_dir, 'accounts.txt')
        self.accounts = {}
        self.load_accounts()

    def load_accounts(self):
        if not os.path.exists(self.account_file):
            return

        with open(self.account_file, 'r') as file:
            for line in file:
                account_number, account_holder, balance, password = line.strip().split(',')
                self.accounts[account_number] = {
                    'account_holder': account_holder,
                    'balance': float(balance),
                    'password': password
                }

    def save_accounts(self):
        with open(self.account_file, 'w') as file:
            for account_number, account_info in self.accounts.items():
                account_holder = account_info['account_holder']
                balance = account_info['balance']
                password = account_info['password']
                file.write(f"{account_number},{account_holder},{balance},{password}\n")

    def create_account(self, account_number, account_holder, initial_balance, password):
        if account_number in self.accounts:
            messagebox.showerror("Error", "Account number already exists.")
        else:
            self.accounts[account_number] = {
                'account_holder': account_holder,
                'balance': initial_balance,
                'password': password
            }
            self.save_accounts()
            messagebox.showinfo("Success", "Account created successfully.")

    def deposit(self, account_number, amount, password):
        if account_number in self.accounts:
            if self.accounts[account_number]['password'] == password:
                self.accounts[account_number]['balance'] += amount
                self.save_accounts()
                messagebox.showinfo("Success", "Deposited successfully.")
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def withdraw(self, account_number, amount, password):
        if account_number in self.accounts:
            if self.accounts[account_number]['password'] == password:
                if self.accounts[account_number]['balance'] >= amount:
                    self.accounts[account_number]['balance'] -= amount
                    self.save_accounts()
                    messagebox.showinfo("Success", "Withdrawn successfully.")
                else:
                    messagebox.showerror("Error", "Insufficient balance.")
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def check_balance(self, account_number, password):
        if account_number in self.accounts:
            if self.accounts[account_number]['password'] == password:
                balance = self.accounts[account_number]['balance']
                return balance
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def close_account(self, account_number, password):
        if account_number in self.accounts:
            if self.accounts[account_number]['password'] == password:
                del self.accounts[account_number]
                self.save_accounts()
                messagebox.showinfo("Success", "Account closed successfully.")
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def list_accounts(self):
        accounts_info = []
        for account_number, account_info in self.accounts.items():
            accounts_info.append(
                f"Account Number: {account_number}, Account Holder: {account_info['account_holder']}, Balance: ${account_info['balance']}"
            )
        return accounts_info

def create_account_callback():
    account_number = account_number_entry.get()
    account_holder = account_holder_entry.get()
    initial_balance = initial_balance_entry.get()
    password = password_entry.get()

    if account_number and account_holder and initial_balance and password:
        bank.create_account(account_number, account_holder, float(initial_balance), password)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def deposit_callback():
    account_number = account_number_entry.get()
    amount = deposit_amount_entry.get()
    password = password_entry.get()

    if account_number and amount and password:
        bank.deposit(account_number, float(amount), password)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def withdraw_callback():
    account_number = account_number_entry.get()
    amount = withdraw_amount_entry.get()
    password = password_entry.get()

    if account_number and amount and password:
        bank.withdraw(account_number, float(amount), password)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def check_balance_callback():
    account_number = account_number_entry.get()
    password = password_entry.get()

    if account_number and password:
        balance = bank.check_balance(account_number, password)
        if balance is not None:
            balance_label.config(text=f"Account balance: ${balance}")
    else:
        messagebox.showerror("Error", "Please fill in the Account Number and Password fields.")

def close_account_callback():
    account_number = account_number_entry.get()
    password = password_entry.get()

    if account_number and password:
        bank.close_account(account_number, password)
    else:
        messagebox.showerror("Error", "Please fill in the Account Number and Password fields.")

def show_all_accounts_callback():
    all_accounts_info = "\n".join(bank.list_accounts())
    top = Toplevel()
    top.title("All Accounts")
    all_accounts_label = tk.Label(top, text=all_accounts_info)
    all_accounts_label.pack()

data_dir = "bank_data"
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

bank = BankSystem(data_dir)

app = tk.Tk()
app.title("Bank Management System")

account_number_label = tk.Label(app, text="Account Number:")
account_number_label.grid(row=0, column=0)
account_number_entry = tk.Entry(app)
account_number_entry.grid(row=0, column=1)

account_holder_label = tk.Label(app, text="Account Holder:")
account_holder_label.grid(row=1, column=0)
account_holder_entry = tk.Entry(app)
account_holder_entry.grid(row=1, column=1)

initial_balance_label = tk.Label(app, text="Initial Balance:")
initial_balance_label.grid(row=2, column=0)
initial_balance_entry = tk.Entry(app)
initial_balance_entry.grid(row=2, column=1)

password_label = tk.Label(app, text="Password:")
password_label.grid(row=3, column=0)
password_entry = tk.Entry(app, show='*')
password_entry.grid(row=3, column=1)

create_account_button = tk.Button(app, text="Create Account", command=create_account_callback)
create_account_button.grid(row=4, column=0, columnspan=2)

deposit_amount_label = tk.Label(app, text="Deposit Amount:")
deposit_amount_label.grid(row=0, column=2)
deposit_amount_entry = tk.Entry(app)
deposit_amount_entry.grid(row=0, column=3)

deposit_button = tk.Button(app, text="Deposit", command=deposit_callback)
deposit_button.grid(row=1, column=2, columnspan=2)

withdraw_amount_label = tk.Label(app, text="Withdraw Amount:")
withdraw_amount_label.grid(row=2, column=2)
withdraw_amount_entry = tk.Entry(app)
withdraw_amount_entry.grid(row=2, column=3)

withdraw_button = tk.Button(app, text="Withdraw", command=withdraw_callback)
withdraw_button.grid(row=3, column=2, columnspan=2)

check_balance_button = tk.Button(app, text="Check Balance", command=check_balance_callback)
check_balance_button.grid(row=4, column=2, columnspan=2)

balance_label = tk.Label(app, text="")
balance_label.grid(row=5, column=0, columnspan=4)

close_account_button = tk.Button(app, text="Close Account", command=close_account_callback)
close_account_button.grid(row=6, column=0, columnspan=4)

show_all_accounts_button = tk.Button(app, text="Show All Accounts", command=show_all_accounts_callback)
show_all_accounts_button.grid(row=7, column=0, columnspan=4)

app.mainloop()
