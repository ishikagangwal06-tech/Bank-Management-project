# Bank Management System

A CLI-based Bank Management System built in Python, designed to perform typical banking operations such as account creation, deposits, withdrawals, fund transfers, and transaction history tracking. It stores data both locally (JSON-based files) and in a PostgreSQL database.

## Project Overview

This project provides a simple CLI interface for clients or administrators to manage banking accounts and log transfer transactions securely. It utilizes bcrypt for hashing user credentials (PINs) and psycopg2 for PostgreSQL database integration.

## Features

- **Account Creation**: Create user accounts with custom validation rules (e.g., age validation and email format verification).
- **Deposits & Withdrawals**: Perform transactions with validation rules (deposit limits, insufficient balance checks).
- **Detail Management**: View account profile details or update fields securely.
- **Fund Transfers**: Direct transfer from a sender to a receiver account using database transactions.
- **Transaction Logs**: Retrieve a detailed list of all transfers made.
- **Data Persistence**: Co-existent JSON and PostgreSQL database storage layers.

## Technologies Used

- **Programming Language**: Python 3
- **Database**: PostgreSQL
- **Security & Cryptography**: Bcrypt (for PIN hashing)
- **Database Connector**: Psycopg2

## Project Structure

```text
Bank-Management-System/
│
├── main.py            # Entry point of the CLI application
├── bank.py            # Core Bank logic and services (Account and transaction actions)
├── database.py        # Database connectivity config and session establishment
├── utils.py           # Reusable utility and validation helper functions
├── requirements.txt   # Third-party library dependencies
├── schema.sql         # SQL schema definitions for PostgreSQL tables
├── README.md          # Project documentation
└── .gitignore         # File/Folder git exclusions
```

## Database Schema

```sql
-- Create account table
CREATE TABLE account (
    account_no INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Create account_list table
CREATE TABLE account_list (
    account_no INTEGER PRIMARY KEY REFERENCES account(account_no) ON DELETE CASCADE,
    balance INTEGER NOT NULL DEFAULT 0,
    pin VARCHAR(255) NOT NULL
);

-- Create transaction table
CREATE TABLE transaction (
    trans_id INTEGER PRIMARY KEY,
    sender_id INTEGER REFERENCES account(account_no) ON DELETE SET NULL,
    reciever_id INTEGER REFERENCES account(account_no) ON DELETE SET NULL,
    amount INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL
);
```

## Installation

1. **Clone/Move into the directory**:
   ```bash
   cd BankManagement
   ```

2. **Install requirements**:
   Ensure you have virtualenv activated or install packages system-wide:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure PostgreSQL**:
   - Ensure PostgreSQL is running.
   - Configure a database named `BankManagement`.
   - Update database credentials (host, port, user, password) inside [database.py](file:///Users/home/Python-practise%20/BankManagement/database.py).
   - Execute SQL commands in [schema.sql](file:///Users/home/Python-practise%20/BankManagement/schema.sql) to initialize your database structure.

## Running the Project

Run the entry script in terminal:
```bash
python main.py
```

## Menu Options

1. **create acount**: Prompts for name, age, email, and 4-digit PIN. Creates and stores the account.
2. **deposit money**: Deposits amount under limits (max 10000) into accounts.
3. **withdraw money**: Withdraws valid funds after validating PIN.
4. **display details**: Shows user account profile details along with current balance.
5. **update details**: Updates name, email, or PIN.
6. **delete acount**: Deletes database records associated with the account.
7. **transfer money**: Direct fund transfer between accounts.
8. **show transactions**: Prints history logs of sender transfers.
9. **Exit**: Gracefully exits the terminal application.

## Security Features

- **PIN Hashing**: User PINs are encoded and hashed with salt using the standard Python `bcrypt` library. No plaintext PINs are saved in the database or files.
- **Validation**:
  - Email addresses are verified against a standardized email format regex.
  - Minimum age constraints require users to be at least 18 years old.

## Future Improvements

- Fully transition legacy JSON filesystem persistence to a unified transactional relational DB framework.
- Handle CLI inputs more gracefully (sanitize menu choice, numeric values, exception messages).
- Add modern REST APIs and a Web UI dashboard.
