MBI Banking System

Overview

MBI Banking System is a Streamlit-based banking application that allows users to:

Create an account

Check balance

Deposit money

Withdraw money

View transaction history

The app ensures secure and seamless transactions using CSV-based data storage with proper error handling.

Features

✅ Create Account – Open an account with a unique account number and an initial deposit.
✅ Check Balance – Instantly view your account balance.
✅ Deposit Money – Securely add funds to your account.
✅ Withdraw Money – Withdraw funds while ensuring sufficient balance.
✅ Transaction History – View the last 5 transactions for better financial tracking.

Technologies Used

Python – Core logic & functionality

Streamlit – Interactive UI

CSV – Data storage

Random & Datetime – Account number generation & timestamps

OS & Exception Handling – File operations & error management

Installation

Clone the repository

git clone https://github.com/yourusername/mbi-banking-system.git
cd mbi-banking-system

Install dependencies

pip install streamlit

Run the application

streamlit run mbi_banking.py

Usage

Navigate through the tabs to perform banking operations.

Ensure correct account number while checking balance or making transactions.

Transactions and account details are stored in CSV files for persistence.

Notes

A minimum deposit of $500 is required to create an account.

Withdrawals require sufficient funds to proceed.

The app operates on local CSV storage, so deleting files will remove data.

Future Enhancements

🚀 Database Integration (MySQL/SQLite) for better storage.
🚀 Authentication System for enhanced security.
🚀 Mobile-Friendly UI with improved design.

License

This project is open-source. Feel free to modify and contribute! 🎉

