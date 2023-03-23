import config as cfg

import telebot

from telebot import types

# Initialization Telegram Bot
TG_Bot = telebot.TeleBot(cfg.API_KEY)


@TG_Bot.message_handler(commands=['start'], content_types=['text'])
def greeting(message):
    # Greeting
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["greeting"])
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["ready"])

    TG_Bot.register_next_step_handler(message, start_registration)


def start_registration(message):
    # Creating Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for answer in cfg.ANSWERS["ready"]:
        buttons += [types.KeyboardButton(answer)]
    markup.add(*buttons)

    TG_Bot.send_message(message.from_user.id, "Заглушка!😀", reply_markup=markup)


if __name__ == "__main__":
    TG_Bot.polling(none_stop=True, interval=0)
