import config as cfg

import telebot

from telebot import types

# Initialization Telegram Bot
TG_Bot = telebot.TeleBot(cfg.API_KEY)

information = []
guests_list = []


@TG_Bot.message_handler(commands=['start'], content_types=['text'])
def greeting(message):
    # Clearing
    information.clear()
    guests_list.clear()

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
    # Adding Info
    global information
    information += [message.text.split()[-1]]

    # Creating Buttons
    markup = types.ReplyKeyboardRemove()

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["name"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, write_number)


def write_number(message):
    # Adding Info
    global information
    information += [message.text.split()[-1]]

    # Creating Buttons
    markup = types.ReplyKeyboardRemove()

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["number"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, choose_city)


def choose_city(message):
    # Adding Info
    global information
    information += [message.text.split()[-1]]

    # Creating Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = []
    for answer in cfg.ANSWERS["city"]:
        buttons += [types.KeyboardButton(answer)]

    markup.add(*buttons)

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["city"], reply_markup=markup)
    add_info(message)


def add_info(message):
    # Adding Info
    global information
    information += [message.text.split()[-1]]

    # Sending Messages
    condition_choose(message)


def condition_choose(message):
    global information

    if information[0] == "Спортсмен":
        TG_Bot.register_next_step_handler(message, choose_sport)

    elif information[3] != "Волгоград" and information[0] in ['Организатор', 'Болельщик', 'Гость']:
        TG_Bot.register_next_step_handler(message, write_hotel_name)


def choose_sport(message):
    # Adding Info
    global information
    information += [message.text.split()[-1]]

    # Creating Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = []
    for answer in cfg.ANSWERS["sport"]:
        buttons += [types.KeyboardButton(answer)]

    markup.add(*buttons)

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["sport"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, choose_sport)


def write_hotel_name(message):
    # Adding Info
    global information
    information += [message.text.split()[-1]]

    # Creating Buttons
    markup = types.ReplyKeyboardRemove()

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["hotel_name"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, write_hotel_number)


def write_hotel_number(message):
    # Adding Info
    global information
    information += [message.text.split()[-1]]

    # Creating Buttons
    markup = types.ReplyKeyboardRemove()

    # Sending Messages
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["hotel_number"], reply_markup=markup)

    TG_Bot.register_next_step_handler(message, write_hotel_number)


if __name__ == "__main__":
    TG_Bot.polling(none_stop=True, interval=0)
