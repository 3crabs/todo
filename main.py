import json

import telebot

with open('telegram_token.json', 'r') as file:
    data = file.read()
config = json.loads(data)

bot = telebot.TeleBot(config["token"])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет я todo bot от 3CRABS soft!\nЧтобы узнать подробности введи /help")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Я пока ничего не умею(")


bot.polling()
