import json

import telebot

with open('telegram_token.json', 'r') as file:
    data = file.read()
config = json.loads(data)

bot = telebot.TeleBot(config["token"])
