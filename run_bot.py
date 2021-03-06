import json
import threading
import time

import schedule
import telebot

from src.TodoBot import TodoBot
from src.models.EveryMonthTimeScheduleItem import EveryMonthTimeScheduleItem
from src.models.ItemState import ItemState
from src.models.OneTimeScheduleItem import OneTimeScheduleItem

config_file_name = 'static/config.json'
try:
    with open(config_file_name, 'r') as file:
        data = file.read()
        config = json.loads(data)
        bot = telebot.TeleBot(config["token"])
        todo_bot = TodoBot("sqlite:///static/todo_bot.db")
except FileNotFoundError as e:
    print(f"File {config_file_name} not found.")
    exit()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет я todo bot от 3CRABS soft!\n"
                                      "Я создаю списки!\n"
                                      "Чтобы узнать подробности введи /help")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id,
                     "Если вы это читаете, значит я забыл написать вам инструкцию. Сообщите мне об этом @vo13crabs")


@bot.message_handler(content_types=["text"])
def content_text(message):
    answer = todo_bot.message_handler(message.text.strip(), str(message.chat.id))
    if answer != '':
        bot.send_message(message.chat.id, answer, parse_mode="HTML")


def schedules():
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_datetime():
    return time.strftime("%d.%m.%Y %H:%M", time.gmtime(time.time() + 7 * 60 * 60))


def get_month_day():
    return time.strftime("%d %H:%M", time.gmtime(time.time() + 7 * 60 * 60))


def one_time_schedule():
    session = todo_bot.get_session()
    items = session.query(OneTimeScheduleItem).filter(
        OneTimeScheduleItem.notification_datetime == get_datetime(),
        OneTimeScheduleItem.state == ItemState.ACTIVE).all()
    for item in items:
        bot.send_message(item.chat_id, item.name)
        item.state = ItemState.DELETE
    session.commit()


def every_month_time_schedule():
    session = todo_bot.get_session()
    items = session.query(EveryMonthTimeScheduleItem).filter(
        EveryMonthTimeScheduleItem.notification_datetime == get_month_day(),
        EveryMonthTimeScheduleItem.state == ItemState.ACTIVE).all()
    for item in items:
        bot.send_message(item.chat_id, item.name)
    session.commit()


if __name__ == '__main__':
    schedule.every(1).minutes.do(one_time_schedule)
    schedule.every(1).minutes.do(every_month_time_schedule)
    thread = threading.Thread(target=schedules)
    thread.start()
    bot.polling()
