import config as cfg

import telebot

from telebot import types

# Initialization Telegram Bot
TG_Bot = telebot.TeleBot(cfg.API_KEY)


@TG_Bot.message_handler(commands=['start'], content_types=['text'])
def greeting(message):
    # Greeting & Start Registration
    TG_Bot.send_message(message.from_user.id, cfg.MESSAGES["greeting"])


if __name__ == "__main__":
    TG_Bot.polling(none_stop=True, interval=0)
