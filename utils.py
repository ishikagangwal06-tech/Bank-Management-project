import re
import random
import bcrypt

def validate_email(email):
    pattern = r"^[a-zA-Z0-9]+@[a-z]+\.[a-z]+$"
    return bool(re.fullmatch(pattern, email))

def generate_account_number():
    return random.randint(10000000, 99999999)

def hash_pin(pin):
    pin_bytes = pin.encode('utf-8')
    hashed_pin = bcrypt.hashpw(pin_bytes, bcrypt.gensalt())
    return hashed_pin.decode('utf-8')

def check_pin(entered_pin, stored_hash):
    return bcrypt.checkpw(
        entered_pin.encode('utf-8'),
        stored_hash.encode('utf-8')
    )

def generate_transaction_id():
    return random.randint(100000000, 999999999)
