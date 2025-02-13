import streamlit as st
import random
import csv
import os
from datetime import datetime

class Transaction:
    def __init__(self, acc_no, transaction_type, amount, balance):
        self.acc_no = acc_no
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance = balance
        self.timestamp = datetime.now()

    def save(self):
        """Save transaction to transactions.csv"""
        try:
            file_exists = os.path.exists("transactions.csv")
            with open("transactions.csv", "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Account", "Type", "Amount", "Balance", "Timestamp"])
                if not file_exists:
                    writer.writeheader()
                writer.writerow({
                    "Account": self.acc_no,
                    "Type": self.transaction_type,
                    "Amount": self.amount,
                    "Balance": self.balance,
                    "Timestamp": self.timestamp
                })
        except Exception as e:
            st.error(f"Failed to save transaction: {e}")

class Bank:
    def __init__(self, acc_no):
        self.acc_no = str(acc_no)
        self._balance = None
        self.name = None
        self.load_account()

    def load_account(self):
        """Load account details from the CSV file."""
        if not os.path.exists("bank.csv"):
            raise ValueError("No accounts exist. Please create an account first.")
            
        with open("bank.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Account Number"] == self.acc_no:
                    self._balance = float(row["Balance"])
                    self.name = row["Name"]
                    return
        raise ValueError("Account not found")

    def check_balance(self, acc_no: str):
        """Check balance for an account."""
        try:
            with open("bank.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Account Number"] == acc_no:
                        name = row["Name"]
                        balance = float(row["Balance"])
                        st.success(f"Hello {name}!")
                        return f"Current balance: ${balance:.2f}"
            # If no matching account is found
            st.error("Account not found")
            return "Account not found"
        except FileNotFoundError:
            st.error("The accounts file does not exist.")
            return "The accounts file does not exist."
        except KeyError as e:
            st.error(f"Invalid CSV format: Missing column {e}")
            return f"Invalid CSV format: Missing column {e}"
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}"


    def update_balance_in_file(self):
        """Update the balance in the CSV file."""
        temp_rows = []
        found = False
        
        with open("bank.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Account Number"] == self.acc_no:
                    row["Balance"] = str(self._balance)
                    found = True
                temp_rows.append(row)
                
        if not found:
            raise ValueError("Account not found")
            
        with open("bank.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Account Number", "Balance"])
            writer.writeheader()
            writer.writerows(temp_rows)

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount
        self.update_balance_in_file()
        
        # Record transaction
        Transaction(self.acc_no, "Deposit", amount, self._balance).save()
        
        return f"Deposited ${amount:.2f}. Current balance: ${self._balance:.2f}"

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        
        self._balance -= amount
        self.update_balance_in_file()
        
        # Record transaction
        Transaction(self.acc_no, "Withdrawal", -amount, self._balance).save()
        
        return f"Withdrew ${amount:.2f}. Current balance: ${self._balance:.2f}"

def create_account():
    """Create a new bank account."""
    with st.form("create_account_form"):
        st.write("### Create New Account")
        name = st.text_input("Enter your name:").strip().title()
        age = st.number_input("Enter your age:", min_value=0, max_value=150, step=1)
        submit = st.form_submit_button("Create Account")
        
        if submit:
            if not name:
                st.error("Name cannot be empty")
                return
            
            if age < 18:
                st.error("Must be 18 or older to open an account")
                return
                
            acc_no = str(random.randint(10**9, 10**10 - 1))
            initial_balance = 500.0
            
            file_exists = os.path.exists("bank.csv")
            
            with open("bank.csv", "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Name", "Account Number", "Balance"])
                writer.writeheader()
                writer.writerow({
                    "Name": name,
                    "Account Number": acc_no,
                    "Balance": initial_balance
                })
            
            st.success("Account created successfully!")
            st.info(f"""
            Please save your account details:
            - Account Number: {acc_no}
            - Initial Balance: ${initial_balance:.2f}
            """)

def view_transactions(acc_no):
    """View transaction history for an account."""
    if not os.path.exists("transactions.csv"):
        st.info("No transactions found")
        return
        
    transactions = []
    with open("transactions.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Account"] == acc_no:
                transactions.append(row)
    
    if transactions:
        st.write("### Transaction History")
        for t in transactions[-5:]:  # Show last 5 transactions
            st.text(f"""
            {t['Timestamp']} | {t['Type']}: ${float(t['Amount']):.2f}
            Balance after transaction: ${float(t['Balance']):.2f}
            """)
    else:
        st.info("No transactions found for this account")

def main():
    st.set_page_config(page_title="MBI Banking System", layout="wide")
    
    st.title("🏦 Welcome to MBI Banking System")
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Create Account", 
        "Check Balance", 
        "Withdraw Money", 
        "Deposit Money",
        "View Transactions"
    ])
    
    with tab1:
        create_account()
        
    with tab2:
        with st.form("check_balance_form"):
            acc_no = st.text_input("Enter your account number (10 digits):")
            submit = st.form_submit_button("Check Balance")
            if submit and acc_no:
                try:
                    bank = Bank(acc_no)
                    st.success(bank.check_balance(acc_no))
                except ValueError as e:
                    st.error(str(e))
    
    with tab3:
        with st.form("withdraw_form"):
            acc_no = st.text_input("Enter your account number (10 digits):", key="withdraw_acc")
            amount = st.number_input("Enter amount to withdraw:", min_value=0.0, step=10.0)
            submit = st.form_submit_button("Withdraw")
            if submit and acc_no:
                try:
                    bank = Bank(acc_no)
                    result = bank.withdraw(amount)
                    st.success(result)
                except ValueError as e:
                    st.error(str(e))
    
    with tab4:
        with st.form("deposit_form"):
            acc_no = st.text_input("Enter your account number (10 digits):", key="deposit_acc")
            amount = st.number_input("Enter amount to deposit:", min_value=0.0, step=10.0)
            submit = st.form_submit_button("Deposit")
            if submit and acc_no:
                try:
                    bank = Bank(acc_no)
                    result = bank.deposit(amount)
                    st.success(result)
                except ValueError as e:
                    st.error(str(e))
    
    with tab5:
        with st.form("transaction_history_form"):
            acc_no = st.text_input("Enter your account number (10 digits):", key="history_acc")
            submit = st.form_submit_button("View Transactions")
            if submit and acc_no:
                try:
                    bank = Bank(acc_no)  # Verify account exists
                    view_transactions(acc_no)
                except ValueError as e:
                    st.error(str(e))

if __name__ == "__main__":
    main()