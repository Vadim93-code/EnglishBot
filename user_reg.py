import sqlite3
import datetime


def user_registration(user_id):
    # make connection to database
    conn = sqlite3.connect('data_base.db')

    # create cursor
    cursor = conn.cursor()

    # get the time when user start use the bot
    reg_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    list_of_user_information = [user_id, reg_date]

    # get all list of users
    cursor.execute('''SELECT user_id from user''')

    rows = cursor.fetchall()

    # if user exist in database we send a message that are happy see they again, if not we registrate user in database
    detector = False
    for row in rows:
        id = row[0]

        if user_id == id:
            detector = True
            print("Welcome back")

    if not detector:
        cursor.execute('''INSERT INTO user (user_id, start_date) VALUES (?, ?)''', list_of_user_information)

    # Save changing
    conn.commit()

    # Close connection
    conn.close()