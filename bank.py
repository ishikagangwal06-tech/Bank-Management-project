import json
import random
from pathlib import Path
from database import connect_db
import utils

class Bank():
    conn = connect_db()
    print("Database Connected Successfully")
    conn.close()

    database='data.json'
    data=[]
    
    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("no such file")
    except Exception as err:
        print("an exception occured",err)

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            json.dump(Bank.data, fs, indent=4)
    
    def createAccount(self):
        info={
            "account_no":utils.generate_account_number(),
            "name":input("tell your name: "),
            "age":int(input("tell your age ")),
            "email":input("tell your email "),
            "balance":0
        }

        pin=input("tell your pin")
        if len(str(pin))!=4:
            print("pin should be 4 characters")
            return
        hashed_pin=utils.hash_pin(pin)
        info2={
            "pin":hashed_pin
        }

        if info['age']<18 :
            print("cannot create account")
            return
        elif not utils.validate_email(info['email']):
            print("invalid email")
            return
        else:
            print("successfully created account")
            for i in info:
                print(f"{i}:{info[i]}")
            print("please note your acc number")
            Bank.data.append(info)
            Bank.__update()

            Bank.data.append(info2)
            Bank.__update()

        conn = connect_db()
        cursor = conn.cursor()


        query = """
        INSERT INTO account
        (account_no,name,age,email)
        VALUES(%s,%s,%s,%s)
        """
        query2="""
        INSERT INTO account_list
        (account_no,balance,pin)
        VALUES(%s,%s,%s)"""



        cursor.execute(
            query,
            (
                info["account_no"],
                info["name"],
                info["age"],
                info["email"]
                
                
            )
        )
        cursor.execute(
            query2,
            (
                info["account_no"],
                info["balance"],
                info2["pin"]
            )
        )


        conn.commit()

        cursor.close()
        conn.close()


        print("Data saved in database")
    

    def deposit(self):

        accnum = int(input("tell your accno: "))
        pin = input("tell your pin: ")
        


        conn = connect_db()
        cursor = conn.cursor()


    # Check account exists
        cursor.execute(
            """
            SELECT * FROM account_list
            WHERE account_no=%s 
            """,
            (accnum,)
        )


        userdata = cursor.fetchone()


        if userdata is None:
            print("No data found")
        else:
            stored_hash = userdata[2]


        # Check PIN using bcrypt
            if not utils.check_pin(pin, stored_hash):

                print("Wrong PIN")


            else:

                amount = int(input("How much do you want to deposit? "))


            if amount > 10000 or amount < 0:
                print("Amount is invalid")


            else:

                cursor.execute(
                """
                UPDATE account_list
                SET balance = balance + %s
                WHERE account_no=%s 
                """,
                (amount, accnum, )
                )


                conn.commit()

                print("Amount deposited successfully")


        cursor.close()
        conn.close()
    


    def withdraw(self):

        accnum = int(input("tell your accno: "))
        pin = input("tell your pin: ")
        

        conn = connect_db()
        cursor = conn.cursor()


    # Check account and get current balance
        cursor.execute(
            """
            SELECT balance,pin FROM account_list
            WHERE account_no=%s 
            """,
            (accnum,)
        )


        userdata = cursor.fetchone()


        if userdata is None:
            print("No data found")
        else:
            stored_hash = userdata[1]


        # Check PIN using bcrypt
            if not utils.check_pin(pin, stored_hash):

                print("Wrong PIN")


            else:

                current_balance = userdata[0]


                amount = int(input("How much do you want to withdraw? "))


            if amount > current_balance:
                print("Insufficient balance")


            elif amount < 0:
                print("Invalid amount")


            else:

                cursor.execute(
                    """
                    UPDATE account_list
                    SET balance = balance - %s
                    WHERE account_no=%s 
                    """,
                    (amount, accnum, )
                )


                conn.commit()

                print("Amount withdrawn successfully")


        cursor.close()
        conn.close()

    def display(self):

        accnum = int(input("Tell your accno: "))
        pin = input("Tell your pin: ")
        


        conn = connect_db()
        cursor = conn.cursor()

        


        cursor.execute(
         """
            SELECT account_no, name, age, email
            FROM account
            WHERE account_no=%s 
        """,
            (accnum,)
        )

        userdata = cursor.fetchone()
        
        cursor.execute(
            """
            SELECT balance,pin FROM account_list
            WHERE account_no=%s 
            """,
            (accnum,)
        )
        userdata2 = cursor.fetchone()

        if userdata is None:
            print("no user found")
        else:
            stored_hash = userdata2[1]


        # Check PIN using bcrypt
            if not utils.check_pin(pin, stored_hash):

                print("Wrong PIN")


            else:

                account = {
                "account_no": userdata[0],
                "name": userdata[1],
                "age": userdata[2],
                "email": userdata[3],
            
                
                }

                cursor.execute(
            """
                SELECT balance
                FROM account_list
                WHERE account_no=%s 
            """,
                (accnum, )
                )

                userdata3 = cursor.fetchone()


                acc2= {
                "balance":userdata3[0],
                }


            for key, value in account.items():
                print(f"{key} : {value}")
            for key, value in acc2.items():
                print(f"{key} : {value}")


        cursor.close()
        conn.close()
    

    def updatedetails(self):

        accnum = int(input("Tell your accno: "))
        pin = input("Tell your pin: ")
        


        conn = connect_db()
        cursor = conn.cursor()


    # Check user exists
        cursor.execute(
        """
        SELECT name,email
        FROM account
        WHERE account_no=%s 
        """,
            (accnum, )
        )


        userdata = cursor.fetchone()

        cursor.execute(
            """
            SELECT balance,pin FROM account_list
            WHERE account_no=%s 
            """,
            (accnum,)
        )
        userdata2 = cursor.fetchone()


        if userdata is None:
            print("pin wrong or no user found")
        else:
            stored_hash = userdata2[1]


        # Check PIN using bcrypt
            if not utils.check_pin(pin, stored_hash):

                print("Wrong PIN")

        print("You cannot change age, account number and balance")
        print("Fill details for change or leave empty if no change")


        new_name = input("Tell new name or press enter: ")
        new_email = input("Tell new email or press enter: ")
        new_pin = input("Tell new pin or press enter: ")


    # Keep old values if empty
        if new_name == "":
            new_name = userdata[0]

        if new_email == "":
            new_email = userdata[1]

        if  new_pin == "":
            new_pin = userdata2[1]
        else:
            new_pin = utils.hash_pin(new_pin)



        cursor.execute(
            """
            UPDATE account
            SET name=%s,
                email=%s
            WHERE account_no=%s 
            """,
            (
            new_name,
            new_email,
            
            accnum,
            
            )
        )

        conn.commit()
        cursor.execute(
            """
            UPDATE account_list
            SET pin=%s
            WHERE account_no=%s 
            """,
            (
            new_pin,
            accnum,
            
            )
        )



        conn.commit()


        print("Updated successfully")


        cursor.close()
        conn.close()

    def delete(self):

        accnum = int(input("Tell your accno: "))
        pin = input("Tell your pin: ")
        


        conn = connect_db()
        cursor = conn.cursor()


    # Check user exists
        cursor.execute(
        """
        SELECT * FROM account
        WHERE account_no=%s 
        """,
        (accnum, )
        )


        userdata = cursor.fetchone()
        cursor.execute(
            """
            SELECT balance,pin FROM account_list
            WHERE account_no=%s 
            """,
            (accnum,)
        )
        userdata2 = cursor.fetchone()


        print("FOUND USER:", userdata)


        if userdata is None:
            print("No data found")
        
        else:
            stored_hash = userdata2[1]


        # Check PIN using bcrypt
            if not utils.check_pin(pin, stored_hash):

                print("Wrong PIN")
            


        check = input("Press y if you want to delete: ")


        if check.lower() == 'y':

            cursor.execute(
            """
            DELETE FROM account
            WHERE account_no=%s 
            """,
                (accnum, )
            )
            cursor.execute(
            """
            DELETE FROM account_list
            WHERE account_no=%s 
            """,
                (accnum, )
            )


            conn.commit()

            print("Deleted successfully")


        else:
            print("Bypassed")


        cursor.close()
        conn.close()


    def transaction(self):

        sender_id = int(input("Enter sender account number: "))
        reciever_id = int(input("Enter receiver account number: "))
        amount = int(input("Enter amount to transfer: "))
        pin = input("Tell your pin: ")
        


        conn = connect_db()
        cursor = conn.cursor()


        cursor.execute(
         """
            SELECT account_no, name, age, email
            FROM account
            WHERE account_no=%s 
        """,
            (sender_id, )
        )


        userdata = cursor.fetchone()
        cursor.execute(
            """
            SELECT balance,pin FROM account_list
            WHERE account_no=%s 
            """,
            (sender_id,)
        )
        userdata2 = cursor.fetchone()
        if userdata is None:
            print("No data found")
        if userdata is None:
            print("pin wrong or no user found")
        else:
            stored_hash = userdata2[1]


        # Check PIN using bcrypt
            if not utils.check_pin(pin, stored_hash):

                print("Wrong PIN")



    # Generate transaction ID
        trans_id = utils.generate_transaction_id()


        conn = connect_db()
        cursor = conn.cursor()


    # Create transaction record first
        cursor.execute(
        """
        INSERT INTO transaction
        (trans_id, sender_id, reciever_id, amount, status)
        VALUES(%s,%s,%s,%s,%s)
        """,
        (
            trans_id,
            sender_id,
            reciever_id,
            amount,
            ""
            )
        )

        conn.commit()



    # Check sender and receiver accounts exist

        cursor.execute(
        """
        SELECT account_no, balance
        FROM account_list
        WHERE account_no IN (%s,%s)
        """,
        (sender_id, reciever_id)
        )


        accounts = cursor.fetchall()



        existing_accounts = [i[0] for i in accounts]


    # If sender or receiver does not exist

        if sender_id not in existing_accounts or reciever_id not in existing_accounts:


            cursor.execute(
            """
            UPDATE transaction
            SET status=%s
            WHERE trans_id=%s
            """,
            (
                "failed",
                trans_id
            )
            )


            conn.commit()

            print("Transaction failed")
            print("Invalid account number")
            print("Transaction ID:", trans_id)


            cursor.close()
            conn.close()
            return



    # Check sender balance

        sender_balance = 0

        for account in accounts:
            if account[0] == sender_id:
                sender_balance = account[1]



        if sender_balance < amount:


            cursor.execute(
            """
            UPDATE transaction
            SET status=%s
            WHERE trans_id=%s
            """,
            (
                "failed",
                trans_id
            )
            )


            conn.commit()

            print("Transaction failed")
            print("Insufficient balance")
            print("Transaction ID:", trans_id)


            cursor.close()
            conn.close()
            return



    # Deduct money from sender

        cursor.execute(
        """
        UPDATE account_list
        SET balance = balance - %s
        WHERE account_no=%s
        """,
        (
            amount,
            sender_id
        )
        )



    # Add money to receiver

        cursor.execute(
        """
        UPDATE account_list
        SET balance = balance + %s
        WHERE account_no=%s
        """,
        (
            amount,
            reciever_id
        )
        )



    # Update transaction status

        cursor.execute(
        """
        UPDATE transaction
        SET status=%s
        WHERE trans_id=%s
        """,
        (
            "success",
            trans_id
        )
            )


        conn.commit()


        print("Transaction successful")
        print("Transaction ID:", trans_id)


        cursor.close()
        conn.close()


    def showtransaction(self):
        accnum=int(input("enter your account"))
        pin = input("Tell your pin: ")
       


        conn = connect_db()
        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT account_no, name, age, email
            FROM account
            WHERE account_no=%s 
            """,
            (accnum, )
        )


        userdata = cursor.fetchone()
        cursor.execute(
            """
            SELECT balance,pin FROM account_list
            WHERE account_no=%s 
            """,
            (accnum,)
        )
        userdata2 = cursor.fetchone()
        if userdata is None:
            print("No data found")
        if userdata is None:
            print("pin wrong or no user found")
        else:
            stored_hash = userdata2[1]


        # Check PIN using bcrypt
            if not utils.check_pin(pin, stored_hash):

                print("Wrong PIN")
        
            else:
                cursor.execute(
                """
                SELECT *
                FROM transaction
                WHERE sender_id=%s
                """,
                (accnum,)
                )

                transactions = cursor.fetchall()
                for transaction in transactions:
                    print(
                    f"""
                    Transaction ID : {transaction[0]}
                    Sender ID      : {transaction[1]}
                    Receiver ID    : {transaction[2]}
                    Amount         : {transaction[3]}
                    Status         : {transaction[4]}
                    """
                )


        cursor.close()
        conn.close()
