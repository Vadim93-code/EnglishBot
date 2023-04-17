import telebot
import PyDictionary
import sqlite3

from telebot import types

from bot_token import BOT_TOKEN
from all_bot_text import START_TEXT

from user_reg import user_registration

bot = telebot.TeleBot(BOT_TOKEN)


# Функция для создания нового списка в базе данных
def create_new_list(user_id, list_name):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("INSERT INTO lists (user_id, list_name) VALUES (?, ?)", (user_id, list_name))
    list_id = c.lastrowid
    conn.commit()
    conn.close()
    return list_id


# Функция для добавления слов в список
def add_words_to_list(list_id, words_list):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    for word in words_list:
        c.execute("INSERT INTO words (list_id, word) VALUES (?, ?)", (list_id, word))
    conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()

    # registrate new customer
    user_id = message.from_user.id
    user_registration(user_id)

    # create and add new button for creating new list of English words
    button_1 = types.KeyboardButton("Create new list of words")
    markup.row(button_1)

    # create and add new button for manage past English words list
    button_2 = types.KeyboardButton("Manage your lists")
    markup.row(button_2)

    bot.send_message(message.chat.id, START_TEXT, reply_markup=markup)

    # create action when user want to create new list
    # bot.register_next_step_handler(message, list_create)


# def list_create(message):
#     if message.text == "Create new list of words":
#         bot.reply_to(message, "Name your list")
#         bot.register_next_step_handler(message, list_create)
#
#     else:
#         bot.reply_to(message, f"Your list with name '{message.text}' created")
#         bot.send_message(message.chat.id, "Send me words which you want add")
#         bot.register_next_step_handler(message, add_words)


# Обработчик нажатия на кнопку "создать новый список"
@bot.message_handler(commands=['newlist'])
def handle_newlist(message):
    user_id = message.from_user.id
    bot.reply_to(message, "Введите имя для нового списка:")
    list_name = message.text
    bot.register_next_step_handler(message, handle_list_name, user_id, list_name)


def handle_list_name(message, user_id, list_name):
    list_name = message.text
    list_id = create_new_list(user_id, list_name)
    bot.reply_to(message, "Новый список создан. Введите слова для добавления в список:")
    words_list = []
    for i in range(30):
        word = input("Введите слово для добавления в список: ")
        if word == "":
            break
        words_list.append(word)
    add_words_to_list(list_id, words_list)
    bot.reply_to(message, "Слова добавлены в список")


# user_word_list = []


# def add_words(message):
#     while True:
#         if message.text == "stop":
#             break
#         else:
#             user_word_list.append(message.text)
#             bot.register_next_step_handler(message, add_words)
#
#         bot.reply_to(message, f"({user_word_list}) Is it all?")


# @bot.message_handler(commands=['create'])
# def create_new_list(message):
#     pass

@bot.message_handler(func=lambda message: True)
def echo(message):
    pass


bot.infinity_polling()