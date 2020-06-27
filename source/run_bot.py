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
    answer = message_handler(message.text.strip(), str(message.chat.id))
    if answer != '':
        bot.send_message(message.chat.id, answer, parse_mode="HTML")


def message_handler(text: str, chat_id: str) -> str:
    if text == '---':
        return delete_all(chat_id)
    if text == '--*':
        return delete_all_mark(chat_id)
    elif text.startswith('++'):
        return add_item(chat_id, text.replace('++', '').strip())
    elif text.startswith('**'):
        return mark_item(text.replace('**', '').strip())
    elif text.startswith('--'):
        return delete_item(text.replace('--', '').strip())
    elif text == '??':
        return get_list(chat_id)


def delete_all(chat_id):
    session = Database.get_instance().session()
    list = session.query(List).filter_by(chat_id=chat_id).first()
    if list:
        items = session.query(Item).filter_by(list_id=list.id).all()
        for item in items:
            item.state = 'delete'
        session.commit()
    return 'Все элементы удалены'


def delete_all_mark(chat_id):
    session = Database.get_instance().session()
    list = session.query(List).filter_by(chat_id=chat_id).first()
    if list:
        items = session.query(Item).filter_by(list_id=list.id, state='mark').all()
        for item in items:
            item.state = 'delete'
        session.commit()
    return 'Все элементы удалены'


def add_item(chat_id, text):
    session = Database.get_instance().session()
    list = session.query(List).filter_by(chat_id=chat_id).first()
    if list is None:
        list = List(chat_id)
    session.add(Item(text, list))
    session.commit()
    return f'Добавлено "{text}"'


def mark_item(text):
    try:
        number = int(text) - 1
    except ValueError:
        return f'"{text}" непохоже на номер в списке'
    session = Database.get_instance().session()
    items = session.query(Item).all()
    if number >= len(items):
        return f'Элемента с номером {number + 1} нет в вашем списке'
    if number < 0:
        return f'Элемента с номером {number + 1} не может быть в вашем списке'
    items[number].state = 'mark'
    session.commit()
    return f'Отмечено "{items[number].name}"'


def get_list(chat_id):
    session = Database.get_instance().session()
    list = session.query(List).filter_by(chat_id=chat_id).first()
    items = session.query(Item).filter_by(list=list).all()
    if not items:
        return 'Список пуст'
    answer = ''
    for i in range(len(items)):
        if items[i].state == 'mark':
            answer += f'<strike>{i + 1}) {items[i].name}</strike>'
        else:
            answer += f'{i + 1}) {items[i].name}'
        if i < len(items) - 1:
            answer += '\n'
    return answer


def delete_item(text):
    try:
        number = int(text) - 1
    except ValueError:
        return f'"{text}" непохоже на номер в списке'
    session = Database.get_instance().session()
    items = session.query(Item).all()
    if number >= len(items):
        return f'Элемента с номером {number + 1} нет в вашем списке'
    if number < 0:
        return f'Элемента с номером {number + 1} не может быть в вашем списке'
    items[number].state = 'mark'
    session.commit()
    return f'Удалено "{items[number].name}"'


if __name__ == '__main__':
    bot.polling()
