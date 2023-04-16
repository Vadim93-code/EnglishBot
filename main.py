import telebot
import PyDictionary

from telebot import types

from bot_token import BOT_TOKEN
from all_bot_text import START_TEXT

from user_reg import user_registration

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()

    user_id = message.from_user.id
    user_registration(user_id)

    button_1 = types.KeyboardButton("Create new list of words")
    markup.row(button_1)

    button_2 = types.KeyboardButton("Manage your lists")
    markup.row(button_2)

    bot.send_message(message.chat.id, START_TEXT, reply_markup=markup)

    bot.register_next_step_handler(message, list_create)


def list_create(message):
    if message.text == "Create new list of words":
        bot.reply_to(message, "Name your list")
        bot.register_next_step_handler(message, list_create)

    else:
        bot.reply_to(message, f"Your list with name '{message.text}' created")


@bot.message_handler(func=lambda message: True)
def create_new_list(message):
    pass


bot.infinity_polling()