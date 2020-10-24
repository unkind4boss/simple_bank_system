
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

class RequestsBD:

    def __init__(self):
        self


    def file_availability(self):
        file_path = "card.s3db"
        return os.path.exists(file_path)


    def create_sql_connect(self, sql_query, loc_values=False, fetch=False):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()

        if loc_values:
            cur.execute(sql_query, loc_values)
        elif fetch:
            cur.execute(sql_query)
            items = cur.fetchall()
            return items
        else:
            cur.execute(sql_query)

        conn.commit()
        conn.close()


    def create_db(self):
        # Executes CREATE TABLE SQL query
        sql = ("""CREATE TABLE card (
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
            )
        """)


    def add_values(self, id, number, pin, balance):
        sql = ("""INSERT INTO card VALUES (?, ?, ?, ?)""")
        values = (id, number, pin, balance)
        create_sql_connect(sql, values)


    def remove_values(self, card_number):
        sql = (f"""DELETE FROM card WHERE number = {card_number}""")
        create_sql_connect(sql)


    # cur.execute('DROP TABLE card')

    def card_num_availability(self, number):
        sql = (f"SELECT * FROM card WHERE number = {number}")
        items = create_sql_connect(sql, fetch=True)
        return items


    def all_select_from_bd(self):
        cur.execute(f"SELECT * FROM card")
        rows = create_sql_connect(sql, fetch=True)
        return rows


    def update_value(self, card_number, new_balance=0, n=1):
        # UPDATE table_name SET col1 = expr1, col2 = expr2, …, colN = expr
        # WHERE logical_expression;
            old_balance = card_num_availability(card_number)

            if n == 1:
                sql = (f"""UPDATE
                                card SET balance = {old_balance[0][3] \
                                                    + new_balance}
                            WHERE
                                number = {card_number}"""
                        )
                create_sql_connect(sql)
            if n == 0:
                sql = (f"""UPDATE
                                    card SET balance = {new_balance}
                                WHERE
                                    number = {card_number}"""
                        )
                create_sql_connect(sql)



class WorkWithBank:

    def __init__(self):
        self


    def card_num_create(self, n):
        back_list = ""
        for _ in range(n):
            back_list += str(random.randrange(0, 9))
        return back_list


    def algo_luhn(self, card_num):
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


    def create_card(self):

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


    def add_income(self, card_number):

        print("\nEnter income:")
        money = int(input())

        update_value(card_number, money)
        print("Income was added!")
        return


    def do_transfer(self, card_number):

        print("\nTransfer\nEnter card number:")
        to_transfer_card_numb = input()

        # get list of information about account from DB
        inform_of_acc = card_num_availability(card_number)

        if int(inform_of_acc[0][1]) == int(to_transfer_card_numb):
            print("\nYou can't transfer money to the same account!")
            return

        loc_last_num = algo_luhn(to_transfer_card_numb[:-1])
        if loc_last_num != int(to_transfer_card_numb[-1]):
            print("\nProbably you made a mistake in the card number.", end=" ")
            print("Please try again!")
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
        update_value(to_transfer_card_numb, transfer_money, 1)
        print("\nSuccess!")
        return
