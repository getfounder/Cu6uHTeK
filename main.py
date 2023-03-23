import config as cfg

import telebot

from telebot import types

# Initialization Telegram Bot
TG_Bot = telebot.TeleBot(cfg.API_KEY)


@TG_Bot.message_handler(commands=['start'], content_types=['text'])
def greeting(message):
    # Greeting
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["greeting"])

    start_registration(message)


def start_registration(message):
    # Creating Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = []
    for answer in cfg.ANSWERS["ready"]:
        buttons += [types.KeyboardButton(answer)]

    markup.add(*buttons)

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["ready"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, choose_category)


def choose_category(message):
    # Creating Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = []
    for answer in cfg.ANSWERS["category"]:
        buttons += [types.KeyboardButton(answer)]

    markup.add(*buttons)

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["category"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, write_name)


def write_name(message):
    # Creating Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["name"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, write_number)


def write_number(message):
    # Creating Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["number"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, write_number)


if __name__ == "__main__":
    TG_Bot.polling(none_stop=True, interval=0)
