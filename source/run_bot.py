import json
import telebot

from source.Database import Database
from source.models.Item import Item
from source.models.List import List

config_file_name = '../static/config.json'
try:
    with open(config_file_name, 'r') as file:
        data = file.read()
        config = json.loads(data)
        bot = telebot.TeleBot(config["token"])
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
    answer = message_handler(message.text.lower().strip(), str(message.chat.id))
    if answer != '':
        bot.send_message(message.chat.id, answer, parse_mode="HTML")


def message_handler(text: str, chat_id: str) -> str:
    if text.startswith('++'):
        return add_item(chat_id, text.replace('++', '').strip())
    elif text.startswith('**'):
        return mark_item(text.replace('**', '').strip())
    elif text.startswith('--'):
        return delete_item(text.replace('--', '').strip())
    elif text == '??':
        return get_list()


def add_item(chat_id, text):
    list = List(chat_id)
    session = Database.get_instance().session()
    session.add(Item(text, list))
    session.commit()
    return f'Добавлено "{text}"'


def mark_item(text):
    number = int(text) - 1
    session = Database.get_instance().session()
    items = session.query(Item).all()
    return f'Отмечено "{items[number].name}"'


def get_list():
    session = Database.get_instance().session()
    items = session.query(Item).all()
    if not items:
        return 'Список пуст'
    answer = ''
    for i in range(len(items)):
        answer += f'{i + 1}) {items[i].name}'
        if i < len(items) - 1:
            answer += '\n'
    return answer


def delete_item(text):
    number = int(text) - 1
    session = Database.get_instance().session()
    items = session.query(Item).all()
    return f'Удалено "{items[number].name}"'


if __name__ == '__main__':
    bot.polling()
