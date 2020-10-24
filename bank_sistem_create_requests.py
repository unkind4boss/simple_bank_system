
import random
import sqlite3
import os.path

from bank_sistem import RequestsBD, WorkWithBank
# sqlite3 datatypes
# NULL
# INTEGER
# REAL
# TEXT
# BLOB

def main(self):

    while True:
        print("\n1. Create an account\n2. Log into account\n0. Exit")
        number_to_login = int(input())

        if number_to_login == 1:
            create_card()


        elif number_to_login == 2:
            typed_card_num = input("Enter your card number:\n")
            typed_pin = input("Enter your PIN:\n")

            # check database, if this typed_card_num has not in DB
            # this list will be empty
            list_data_from_db = card_num_availability(typed_card_num)

            if (bool(list_data_from_db)
                    and list_data_from_db[0][2] == typed_pin):

                print("\nYou have successfully logged in!")
                while True:
                    print("\n1. Balance\n2. Add income\n3. Do transfer")
                    print("4. Close account\n5. Log out\n0. Exit")
                    choose_num_in = int(input())

                    if choose_num_in == 1:
                        print(f"Balance: {list_data_from_db[0][3]}")

                    elif choose_num_in == 2:
                        add_income(typed_card_num)

                    elif choose_num_in == 3:
                        do_transfer(typed_card_num)

                    elif choose_num_in == 4:
                        remove_values(typed_card_num)

                    elif choose_num_in == 5:
                        print("\nYou have successfully logged out!")
                        break

                    elif choose_num_in == 0:
                        print("\nBye!")
                        exit()

                    else:
                        print("\nsmth wrong in second loop")
            else:
                print("\nWrong card number or PIN!")

        elif number_to_login == 0:
            print("\nBye!")
            exit()

        else:
            print("\nsmth wrong")


if __name__ == '__main__':
    try:
        if not file_availability():
            create_db()
        main()
    except KeyboardInterrupt:
        print('ancelled')
