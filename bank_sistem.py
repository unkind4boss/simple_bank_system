
import random

begin_num_card = 400000
dict_logins = dict()
last_num = 0

def card_num_create(n):
    back_list = ""
    for _ in range(n):
        back_list += str(random.randrange(0, 9))
    return back_list

def algo_luhn(card_num):
    sum_all = 0
    card_num = list(card_num)

    for i in range(0, len(card_num), 2):
        card_num[i] = int(card_num[i]) * 2
        if len(str(card_num[i])) == 2:
            doub_num = str(card_num[i])
            sum_ = int(doub_num[0]) + int(doub_num[1])
            card_num[i] = sum_

    print("card_num", card_num)
    for value in card_num:
        sum_all += int(value)

    if sum_all % 10 == 0:
        return 0
    else:
        j = 0
        while sum_all % 10 != 0:
            sum_all += 1
            j += 1
        return j

while True:
    number_to_login = int(input("""\n1. Create an account
2. Log into account
0. Exit
"""))

    if number_to_login == 1:

        med_nums = card_num_create(9)
        created_pin = card_num_create(4)
        last_num = algo_luhn(f"{begin_num_card}{med_nums}")
        created_card_namber = f"{begin_num_card}{med_nums}{last_num}"

        print("\nYour card has been created")
        print(f"Your card number:\n{created_card_namber}")
        print(f"Your card PIN:\n{created_pin}")

        dict_logins[created_card_namber] = created_pin
        balance = 0

    elif number_to_login == 2:
        typed_card_num = input("Enter your card number:\n")
        typed_pin = input("Enter your PIN:\n")

        if typed_card_num in dict_logins and dict_logins[typed_card_num] == typed_pin:
            print("\nYou have successfully logged in!")

            while True:
                choose_num_in = int(input("\n1. Balance\n2. Log out\n0. Exit\n"))

                if choose_num_in == 1:
                    print(f"Balance: {balance}")
                    # continue

                elif choose_num_in == 2:
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
