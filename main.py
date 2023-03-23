import config as cfg

import telebot
from telebot import types

import qrcode


bot = telebot.TeleBot(cfg.API_KEY)

information = []
guests_list = []


@bot.message_handler(commands=['start'], content_types=['text'])
def start(message):
    # Working With Variables
    global information
    global guests_list  

    guests_list.clear()
    information.clear()
    
    # Creating Buttons 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = []
    for city in cfg.ANSWERS["category"]:
        buttons += [types.KeyboardButton(city)]

    markup.add(*buttons)

    # Sending Messages
    bot.send_message(message.from_user.id, cfg.MESSAGES["greeting"])

    bot.send_message(message.from_user.id, cfg.MESSAGES["category"], reply_markup=markup)
    bot.register_next_step_handler(message, choose_category)


def choose_category(message):
    # Working With Variables
    global information
    information += [message.text.split()[-1]]

    # Deleting Buttons 
    markup = types.ReplyKeyboardRemove()

    # Sending Messages
    bot.send_message(message.from_user.id, cfg.MESSAGES["name"], reply_markup=markup)
    bot.register_next_step_handler(message, write_name)


def write_name(message):
    # Working With Variables
    global information
    information += [message.text.split()[-1]]

    # Deleting Buttons 
    markup = types.ReplyKeyboardRemove()

    # Sending Messages
    bot.send_message(message.from_user.id, cfg.MESSAGES["number"], reply_markup=markup)
    bot.register_next_step_handler(message, write_number)


def write_number(message):
    # Working With Variables
    global information
    information += [message.text.split()[-1]]

    # Creating Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    buttons = []
    for city in cfg.ANSWERS["city"]:
        buttons += [types.KeyboardButton(city)]

    markup.add(*buttons)

    # Sending Messages
    bot.send_message(message.from_user.id, cfg.MESSAGES["city"], reply_markup=markup)
    bot.register_next_step_handler(message, choose_city)


def choose_city(message):
    # Working With Variables
    global information
    information += [message.text.split()[-1]]

    if information[0] == 'Спортсмен':
        # Creating Buttons
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        buttons = []
        for sport in cfg.ANSWERS["sport"]:
            buttons += [types.KeyboardButton(sport)]

        markup.add(*buttons)

        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["sport"], reply_markup=markup)
        bot.register_next_step_handler(message, choose_sport)

    elif information[3] != "Волгоград" and information[0] in ['Организатор', 'Болельщик']:
        # Deleting Buttons 
        markup = types.ReplyKeyboardRemove()

        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["hotel_name"], reply_markup=markup)
        bot.register_next_step_handler(message, write_hotel_name)

    else:
        # Creating Buttons
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        buttons = []
        for sport in cfg.ANSWERS["choose_guests"]:
            buttons += [types.KeyboardButton(sport)]

        markup.add(*buttons)

        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["choose_guests"], reply_markup=markup)
        bot.register_next_step_handler(message, choose_guests)


def choose_sport(message):
    # Working With Variables
    global information
    information += [message.text.split()[-1]]

    # Deleting Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup = types.ReplyKeyboardRemove()
    
    if information[3] != "Волгоград":
        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["hotel_name"], reply_markup=markup)
        bot.register_next_step_handler(message, write_hotel_name)
    else:
        # Creating Buttons 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        buttons = []
        for city in cfg.ANSWERS["choose_guests"]:
            buttons += [types.KeyboardButton(city)]

        markup.add(*buttons)

        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["choose_guests"], reply_markup=markup)
        bot.register_next_step_handler(message, choose_guests)


def write_hotel_name(message):
    # Working With Variables
    global information
    information += [message.text.split()[-1]]

    # Deleting Buttons 
    markup = types.ReplyKeyboardRemove()

    # Sending Messages
    bot.send_message(message.from_user.id, cfg.MESSAGES["hotel_number"], reply_markup=markup)
    bot.register_next_step_handler(message, write_hotel_number)


def write_hotel_number(message):
    # Working With Variables
    global information
    information += [message.text.split()[-1]]

    # Creating Buttons 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = []
    for city in cfg.ANSWERS["choose_guests"]:
        buttons += [types.KeyboardButton(city)]

    markup.add(*buttons)

    # Sending Messages
    bot.send_message(message.from_user.id, cfg.MESSAGES["choose_guests"], reply_markup=markup)
    bot.register_next_step_handler(message, choose_guests)


def choose_guests(message):
    # Deleting Buttons 
    markup = types.ReplyKeyboardRemove()

    if message.text == "Да":
        # Sending Messages
        bot.send_message(message.from_user.id, cfg.MESSAGES["write_guests"], reply_markup=markup)
        bot.register_next_step_handler(message, write_guests)
    else:
        process_final_step(message)


def write_guests(message):
    # Working With Variables
    global information
    global guests_list

    information += [message.text.split()[-1]]
    guests_list += message.text.split(', ')

    process_final_step(message)


def process_final_step(message):
    # Deleting Buttons 
    markup = types.ReplyKeyboardRemove()

    qr_info = f"{information[0]}\n{information[1]}\n{information[3]}"

    qrcode.make(qr_info).save("temps/qrcode.png")

    bot.send_message(message.from_user.id, cfg.MESSAGES["QR_code"], reply_markup=markup)
    bot.send_photo(message.from_user.id, open("temps/qrcode.png", 'rb'))


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)