-- SQL Schema for Bank Management System

-- Create account table
CREATE TABLE IF NOT EXISTS account (
    account_no INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Create account_list table
CREATE TABLE IF NOT EXISTS account_list (
    account_no INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL DEFAULT 0,
    pin VARCHAR(255) NOT NULL,
    FOREIGN KEY (account_no) REFERENCES account(account_no) ON DELETE CASCADE
);

-- Create transaction table
CREATE TABLE IF NOT EXISTS transaction (
    trans_id INTEGER PRIMARY KEY,
    sender_id INTEGER,
    reciever_id INTEGER,
    amount INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES account(account_no) ON DELETE SET NULL,
    FOREIGN KEY (reciever_id) REFERENCES account(account_no) ON DELETE SET NULL
);
