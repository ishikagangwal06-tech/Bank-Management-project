import psycopg2

def connect_db():

    connection = psycopg2.connect(
        host="localhost",
        database="BankManagement",
        user="postgres",
        password="1234",
        port="5433"
    )

    return connection