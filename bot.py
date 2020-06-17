import json
import telebot

config_file_name = 'telegram_token.json'
try:
    with open(config_file_name, 'r') as file:
        data = file.read()
except FileNotFoundError as e:
    print(f"File {config_file_name} not found.")
    exit()
config = json.loads(data)

bot = telebot.TeleBot(config["token"])

data_base_lists = {}
bot.data_base_subscriptions = {}

try:
    data_base_lists_file_name = 'data_base.json'
    with open(data_base_lists_file_name, 'r') as file:
        data = file.read()
    data_base_lists = json.loads(data)

    data_base_subscriptions_file_name = 'data_base_subscriptions.json'
    with open(data_base_subscriptions_file_name, 'r') as file:
        data = file.read()
    data_base_subscriptions_file_name = json.loads(data)
except FileNotFoundError as e:
    pass


def save_lists():
    with open("data_base.json", "w") as write_file:
        json.dump(data_base_lists, write_file)


def save_subscriptions():
    with open("data_base_subscriptions.json", "w") as write_file:
        json.dump(data_base_subscriptions_file_name, write_file)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет я todo bot от 3CRABS soft!\n"
                                      "Чтобы узнать подробности введи /help")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Когда общаешься со мной у тебя есть личный список. Это удобно!\n"
                                      "Но меня можно добавить в беседу, "
                                      "и тогда будет список специально для вашей беседы. Круто!\n\n"
                                      "Напиши:\n"
                                      "бот добавь {название пункта}\n"
                                      "бот удали {номер пункта}\n"
                                      "бот зачеркни {номер пункта}\n"
                                      "бот покажи список\n\n"

                                      "Или напиши сокращенно:\n"
                                      "++ {название пункта} (добавление)\n"
                                      "-- {номер пункта} (удаление)\n"
                                      "** {номер пункта} (зачеркивание)\n"
                                      "?? (просмотр)\n\n"

                                      "Или команды:\n"
                                      "/start - привет бот\n"
                                      "/help - помощь\n"
                                      "/list - показ списка\n")


@bot.message_handler(commands=["list"])
def send_list(message):
    bot.send_message(message.chat.id, content_text_answer('бот покажи список', str(message.chat.id)), parse_mode='HTML')


@bot.message_handler(content_types=["text"])
def content_text(message):
    print(f'От {message.from_user.first_name} в {message.chat.title} пришло {message.text}')
    answer, keyboard = content_text_answer(message.text.lower().strip(), str(message.chat.id))
    if answer != '':
        if keyboard:
            bot.send_message(message.chat.id, answer, parse_mode="HTML", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, answer, parse_mode="HTML")


def content_text_answer(text: str, chat_id: str):
    answer = ''

    if text == '+' or text == '-' or text == 'бот добавь' or text == 'бот удали':
        return '', None

    if text == 'бот покажи список' or text == '??':
        if chat_id not in data_base_lists:
            return 'Ваш список пока пуст', None
        if data_base_lists[chat_id]:
            answer += 'Ваш список\n'
            for i in range(len(data_base_lists[chat_id])):
                item_text = f'{i + 1}) {data_base_lists[chat_id][i]["title"]}'
                if data_base_lists[chat_id][i]["done"]:
                    item_text = f'<strike>{item_text}</strike>'
                answer += f'{item_text}\n'
            return answer, None
    elif text == 'бот покажи меню':
        return 'Меню', None
    elif text.startswith('бот добавь') or text.startswith('++'):
        if text.startswith('бот добавь'):
            text = text.replace('бот добавь', '').strip()
        else:
            text = text.replace('++', '').strip()

        if text == '':
            return '', None

        if chat_id not in data_base_lists:
            data_base_lists[chat_id] = []
        for word in text.split():
            answer += word + ' '
        data_base_lists[chat_id].append({"title": answer.strip(), "done": False})
        answer += 'добавлено'
        save_lists()
    elif text.startswith('бот удали') or text.startswith('--'):
        if text.startswith('бот удали'):
            text = text.replace('бот удали', '').strip()
        else:
            text = text.replace('--', '').strip()

        if text == '':
            return '', None

        try:
            number = int(text.split()[0]) - 1
        except ValueError:
            return f'{text.split()[0]} это не номер в списке', None
        if chat_id in data_base_lists and len(data_base_lists[chat_id]) > number:
            answer += data_base_lists[chat_id][number]["title"]
            data_base_lists[chat_id].pop(number)
            if not data_base_lists[chat_id]:
                data_base_lists.pop(chat_id)
            answer += ' удалено'
            save_lists()
        else:
            return f'Элемента №{number + 1} нет', None
    elif text.startswith('бот зачеркни') or text.startswith('**'):
        if text.startswith('бот зачеркни'):
            text = text.replace('бот зачеркни', '').strip()
        else:
            text = text.replace('**', '').strip()

        if text == '':
            return '', None

        try:
            number = int(text.split()[0]) - 1
        except ValueError:
            return f'{text.split()[0]} это не номер в списке'
        if chat_id in data_base_lists and len(data_base_lists[chat_id]) > number:
            answer += data_base_lists[chat_id][number]["title"]
            data_base_lists[chat_id][number]["done"] = True
            answer += ' зачеркнуто'
            save_lists()
        else:
            return f'Элемента №{number + 1} нет', None
    else:
        return '', None

    return answer, None


if __name__ == '__main__':
    save_lists()
    save_subscriptions()
    bot.polling()
