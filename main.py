import config as cfg
from functions import *

import telebot
from telebot import types

import qrcode


bot = telebot.TeleBot(cfg.API_KEY)

information = dict()

@bot.message_handler(commands=['start'], content_types=['text'])
def start(message):
    # Working With Variables
    global information
    information[message.from_user.id] = {
        "category": "",
        "name": "",
        "number": "", 
        "city": "", 
        "sport": "", 
        "hotel_name": "", 
        "hotel_number": "", 
        "guests": "",      
    }
    
    # Creating Buttons 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = []
    for city in cfg.ANSWERS["category"]:
        buttons += [types.KeyboardButton(city)]

    markup.add(*buttons)

    # Sending Messages
    if len(information[message.from_user.id]["category"]) == 0:
        bot.send_message(message.from_user.id, cfg.MESSAGES["greeting"])

    bot.send_message(message.from_user.id, cfg.MESSAGES["category"], reply_markup=markup)
    bot.register_next_step_handler(message, choose_category)


def choose_category(message):
    # Working With Variables
    global information
    information[message.from_user.id]["category"] += message.text.split()[-1]

    # Deleting Buttons 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Заново"))

    if information[message.from_user.id]["category"] == "Организатор":
        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["password"], reply_markup=markup)
        bot.register_next_step_handler(message, check_pass)
    else:
        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["name"], reply_markup=markup)
        bot.register_next_step_handler(message, write_name)


def check_pass(message):
    # Working With Variables
    if message.text == "Заново":
        start(message)
    else:
        password = message.text
        # Deleting Buttons 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Заново"))
        
        try:
            if compute(password):
                # Sending Messages
                bot.send_message(message.from_user.id, cfg.MESSAGES["name"], reply_markup=markup)
                bot.register_next_step_handler(message, write_name)
            else:
                bot.send_message(message.from_user.id, cfg.MESSAGES["repassword"], reply_markup=markup)
                bot.register_next_step_handler(message, check_pass)
        except Exception:
            start(message)


def write_name(message):
    if message.text == "Заново":
        start(message)
    else:
        # Working With Variables
        global information
        information[message.from_user.id]["name"] += message.text

        # Deleting Buttons 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Заново"))

        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["number"], reply_markup=markup)
        bot.register_next_step_handler(message, write_number)


def write_number(message):
    if message.text == "Заново":
        start(message)
    else:
        # Working With Variables
        global information
        information[message.from_user.id]["number"] += message.text

        if information[message.from_user.id]["category"] == "Волонтер":
            # Creating Buttons
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            buttons = []
            for sport in cfg.ANSWERS["choose_guests"] + ["Заново"]:
                buttons += [types.KeyboardButton(sport)]

            markup.add(*buttons)

            # Sending Messages
            bot.send_message(message.from_user.id, cfg.MESSAGES["choose_guests"], reply_markup=markup)
            bot.register_next_step_handler(message, choose_guests)
        else:
            # Creating Buttons
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            
            buttons = []
            for city in cfg.ANSWERS["city"] + ["Заново"]:
                buttons += [types.KeyboardButton(city)]

            markup.add(*buttons)

            # Sending Messages
            bot.send_message(message.from_user.id, cfg.MESSAGES["city"], reply_markup=markup)
            bot.register_next_step_handler(message, choose_city)


def choose_city(message):
    if message.text == "Заново":
        start(message)
    else:
        # Working With Variables
        global information
        information[message.from_user.id]["city"] += message.text

        if information[message.from_user.id]["category"] == 'Спортсмен' and information[message.from_user.id]["city"] != "Волгоград":
            # Creating Buttons
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            buttons = []
            for sport in cfg.ANSWERS["sport"] + ["Заново"]:
                buttons += [types.KeyboardButton(sport)]

            markup.add(*buttons)

            # Sending Messages
            bot.send_message(message.from_user.id, cfg.MESSAGES["sport"], reply_markup=markup)
            bot.register_next_step_handler(message, choose_sport)

        elif information[message.from_user.id]["city"] != "Волгоград" and information[message.from_user.id]["category"] in ['Организатор', 'Болельщик']:
            # Deleting Buttons 
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Заново"))

            # Sending Messages
            bot.send_message(message.from_user.id, cfg.MESSAGES["hotel_name"], reply_markup=markup)
            bot.register_next_step_handler(message, write_hotel_name)

        else:
            # Creating Buttons
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            buttons = []
            for sport in cfg.ANSWERS["choose_guests"] + ["Заново"]:
                buttons += [types.KeyboardButton(sport)]

            markup.add(*buttons)

            # Sending Messages
            bot.send_message(message.from_user.id, cfg.MESSAGES["choose_guests"], reply_markup=markup)
            bot.register_next_step_handler(message, choose_guests)


def choose_sport(message):
    if message.text == "Заново":
        start(message)
    else:
        # Working With Variables
        global information
        information[message.from_user.id]["sport"] += " ".join(message.text.split()[1::])

        # Deleting Buttons
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Заново"))
        
        if information[message.from_user.id]["city"] != "Волгоград":
            # Sending Messages
            bot.send_message(message.from_user.id, cfg.MESSAGES["hotel_name"], reply_markup=markup)
            bot.register_next_step_handler(message, write_hotel_name)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            buttons = []
            for city in cfg.ANSWERS["choose_guests"] + ["Заново"]:
                buttons += [types.KeyboardButton(city)]

            markup.add(*buttons)

            # Sending Messages
            bot.send_message(message.from_user.id, cfg.MESSAGES["choose_guests"], reply_markup=markup)
            bot.register_next_step_handler(message, choose_guests)


def write_hotel_name(message):
    if message.text == "Заново":
        start(message)
    else:
        # Working With Variables
        global information
        information[message.from_user.id]["hotel_name"] += message.text

        # Deleting Buttons 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Заново"))

        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["hotel_number"], reply_markup=markup)
        bot.register_next_step_handler(message, write_hotel_number)


def write_hotel_number(message):
    if message.text == "Заново":
        start(message)
    else:
        # Working With Variables
        global information
        information[message.from_user.id]["hotel_number"] += message.text

        # Creating Buttons 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        buttons = []
        for city in cfg.ANSWERS["choose_guests"] + [""]:
            buttons += [types.KeyboardButton(city)]

        markup.add(*buttons)

        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["choose_guests"], reply_markup=markup)
        bot.register_next_step_handler(message, choose_guests)


def choose_guests(message):
    if message.text == "Заново":
        start(message)
    else:
        # Deleting Buttons 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Заново"))

        if message.text == "Да":
            # Sending Messages
            bot.send_message(message.from_user.id, cfg.MESSAGES["write_guests"], reply_markup=markup)
            bot.register_next_step_handler(message, write_guests)
        else:
            process_final_step(message)


def write_guests(message):
    if message.text == "Заново":
        start(message)
    else:
        # Working With Variables
        global information
        information[message.from_user.id]["guests"] += message.text

        process_final_step(message)


def process_final_step(message):
    global information

    # Deleting Buttons 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Продолжить"), types.KeyboardButton("Заново"))

    text = f"""Категория - {information[message.from_user.id]["category"]}\n
ФИО Участника - {information[message.from_user.id]["name"]}\n
Номер телефона - {information[message.from_user.id]["number"]}\n
Команда/регион - {information[message.from_user.id]["city"]}\n
Вид спорта - {information[message.from_user.id]["sport"]}\n
Название отеля - {information[message.from_user.id]["hotel_name"]}\n
Номер комнаты - {information[message.from_user.id]["hotel_number"]}\n
Приглашенные гости - {information[message.from_user.id]["guests"]}
"""

    bot.send_message(message.from_user.id, text, reply_markup=markup)
    bot.send_message(message.from_user.id, cfg.MESSAGES["true"], reply_markup=markup)
    bot.register_next_step_handler(message, adding_info)


def adding_info(message):
    if message.text == "Заново":
        start(message)
    else:
        markup = types.ReplyKeyboardRemove()

        user_data = {
            'A': message.from_user.id,
            'B': information[message.from_user.id]["category"],
            'C': information[message.from_user.id]["name"],
            'D': information[message.from_user.id]["number"],
            'E': information[message.from_user.id]["city"],
            "F": information[message.from_user.id]["sport"],
            'G': information[message.from_user.id]["hotel_name"],
            'H': information[message.from_user.id]["hotel_number"],
            'I': information[message.from_user.id]["guests"],
        }

        bot.send_message(message.from_user.id, cfg.MESSAGES["await"], reply_markup=markup)
        # add_info(user_data)
        
        qr_info = f"{information[message.from_user.id]['category']}\n{information[message.from_user.id]['name']}\n{information[message.from_user.id]['city']}"

        qrcode.make(qr_info).save("temps/qrcode.png")

        bot.send_message(message.from_user.id, cfg.MESSAGES["QR_code"], reply_markup=markup)
        bot.send_photo(message.from_user.id, open("temps/qrcode.png", 'rb'))

        bot.send_message(message.from_user.id, cfg.MESSAGES["Location"], reply_markup=markup)
        bot.send_location(message.from_user.id, *cfg.COORDS)

        bot.send_message(message.from_user.id, cfg.MESSAGES["Booklet"], reply_markup=markup)
        bot.send_document(message.from_user.id, open("data/sample.pdf", 'rb'))

        if information[message.from_user.id]["category"] == "Организатор":
            bot.send_message(message.from_user.id, cfg.MESSAGES["sheet"], reply_markup=markup)

        del information[message.from_user.id]


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)