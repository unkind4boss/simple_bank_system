
import random
import sqlite3
import os.path

# sqlite3 datatypes
# NULL
# INTEGER
# REAL
# TEXT
# BLOB

# DELETE FROM statement
# DELETE FROM books WHERE quantity = 0

def file_availability():
    file_path = "card.s3db"
    return os.path.exists(file_path)


def create_db():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    # Executes CREATE TABLE SQL query
    cur.execute("""CREATE TABLE card (
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0)
        """)
        # id INTEGER,

    conn.commit()
    conn.close()


def add_values(id, number, pin, balance):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute("""INSERT INTO card
                VALUES (?, ?, ?, ?)""",
                (id, number, pin, balance)
            )

    conn.commit()
    conn.close()


def remove_values(card_number):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute(f"""DELETE FROM card WHERE number = {card_number}""")

    conn.commit()
    conn.close()

# cur.execute('DROP TABLE card')

def card_num_availability(number):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM card WHERE number = {number}")

    items = cur.fetchall()
    # print(items)

    conn.commit()
    conn.close()
    return items


def all_select_from_bd():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM card")
    rows = cur.fetchall()

    conn.commit()
    conn.close()
    return rows



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

    # print("card_num", card_num)
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


def create_card():

    begin_num_card = 400000
    # dict_logins = dict()
    last_num = 0
    # creating full card number with Luhn algorithm
    med_nums = card_num_create(9)
    last_num = algo_luhn(f"{begin_num_card}{med_nums}")
    created_card_namber = f"{begin_num_card}{med_nums}{last_num}"

    # creating pin
    created_pin = card_num_create(4)
    balance = 0

    # id_calc = len(c.fetchall()) + 1
    id_ = len(all_select_from_bd()) + 1
    # add values to database
    add_values(id_, created_card_namber, created_pin, balance)

    print("\nYour card has been created")
    print(f"Your card number:\n{created_card_namber}")
    print(f"Your card PIN:\n{created_pin}")


def add_income(card_number):
    #
    print("\nEnter income:")
    money = int(input())
    #
    update_value(card_number, money)
    print("Income was added!")
    return


def update_value(card_number, new_balance=0, n=1):
    # UPDATE table_name SET col1 = expr1, col2 = expr2, …, colN = expr
    # WHERE logical_expression;
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        old_balance = card_num_availability(card_number)

        if n == 1:
            cur.execute(f"""UPDATE
                                card SET balance = {old_balance[0][3]+new_balance}
                            WHERE
                                number = {card_number}"""
                    )
        if n == 0:
            cur.execute(f"""UPDATE
                                card SET balance = {new_balance}
                            WHERE
                                number = {card_number}"""
                    )


        conn.commit()
        conn.close()


def do_transfer(card_number):

    print("\nTransfer\nEnter card number:")
    to_transfer_card_numb = input()
    # HERE MAY BE MISTAKE
    # print("Enter how much money you want to transfer:")
    # transfer_money = int(input())

    # get list of information about account from DB
    inform_of_acc = card_num_availability(card_number)

    # if inform_of_acc[0][3] < transfer_money:
    #     print("Not enough money!")
    #     return

    if int(inform_of_acc[0][1]) == int(to_transfer_card_numb):
        print("\nYou can't transfer money to the same account!")
        return

    loc_last_num = algo_luhn(to_transfer_card_numb[:-1])
    if loc_last_num != int(to_transfer_card_numb[-1]):
        print("\nProbably you made a mistake in the card number. Please try again!")
        return

    if not card_num_availability(to_transfer_card_numb):
        print("\nSuch a card does not exist.")
        return

    print("\nEnter how much money you want to transfer:")
    transfer_money = int(input())

    if inform_of_acc[0][3] < transfer_money:
        print("\nNot enough money!")
        return
    #
    update_value(card_number, inform_of_acc[0][3] - transfer_money, 0)
    #
    # old_balance_in_to_trans_card = card_num_availability(to_transfer_card_numb)
    update_value(to_transfer_card_numb, transfer_money, 1)
                 # + old_balance_in_to_trans_card[0][3])
    print("\nSuccess!")
    return




def main():

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





# if not file_availability():
#     create_db()
#
# conn = sqlite3.connect('card.s3db')
# cur = conn.cursor()
#
# # cur.execute('DROP TABLE card')
#
# conn.commit()
# conn.close()


# a =  card_num_availability("4000003533628539")

# print(a)
# update_value("4000003533628539", 20)
# list_ = card_num_availability('1999')
# print(list_[0][3])
# print(all_select_from_bd())



# values_ = all_select_from_bd()
#
# for item in values_:
#     print(item)

if __name__ == '__main__':
    try:
        if not file_availability():
            create_db()
        main()
    except KeyboardInterrupt:
        print('ancelled')



# card_num_availability("1999")
# add_values(0, "1999", "1888", 0)
# add_values(1, "2999", "2888", 10)
# add_values(2, "3999", "3888", 15)
