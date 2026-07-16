import psycopg2

def connect_db():

    connection = psycopg2.connect(
        host="localhost",
        database="BankManagement",
        user="postgres",
        password="[PASSWORD]"
        port=" "
    )

    return connection