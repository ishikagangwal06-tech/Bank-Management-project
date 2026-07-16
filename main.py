from bank import Bank

user=Bank()
check=0
print("----BANK MANAGEMENT PROJECT----")
while check!=9:
    print("press 1: create acount")
    print("press 2: deposit money")
    print("press 3: withdraw money")
    print("press 4: display details")
    print("press 5: update details")
    print("press 6: delete acount")
    print("press 7: transfer money")
    print("press 8: show transactions ")
    print("press 9: Exit")

    check=int(input("enter your choice "))

    if check==1:
        user.createAccount()

    if check==2:
        user.deposit()

    if check==3:
        user.withdraw()

    if check==4:
        user.display()

    if check==5:
        user.updatedetails()

    if check==6:
        user.delete()
    
    if check==7:
        user.transaction()
    
    if check==8:
        user.showtransaction()

    if check==9:
        break