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

data_base = {}
try:
    data_base_file_name = 'data_base.json'
    with open(data_base_file_name, 'r') as file:
        data = file.read()
    data_base = json.loads(data)
except FileNotFoundError as e:
    pass


def save():
    with open("data_base.json", "w") as write_file:
        json.dump(data_base, write_file)


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
                                      "бот покажи список\n\n"

                                      "Или напиши сокращенно:\n"
                                      "+ {название пункта} (добавление)\n"
                                      "- {номер пункта} (удаление)\n"
                                      ". (просмотр)\n\n"

                                      "Или команды:\n"
                                      "/start - привет бот\n"
                                      "/help - помощь\n"
                                      "/list - показ списка\n")


@bot.message_handler(commands=["list"])
def send_list(message):
    bot.send_message(message.chat.id, content_text_answer('бот покажи список', str(message.chat.id)))


@bot.message_handler(content_types=["text"])
def content_text(message):
    answer = content_text_answer(message.text.lower().strip(), str(message.chat.id))
    if answer != '':
        bot.send_message(message.chat.id, answer)


def content_text_answer(text: str, chat_id: str) -> str:
    answer = ''

    if text == '+' or text == '-' or text == 'бот добавь' or text == 'бот удали':
        return ''

    if text == 'бот покажи список' or text == '.':
        if chat_id not in data_base:
            return 'Ваш список пока пуст'
        if data_base[chat_id]:
            answer += 'Ваш список\n'
            for i in range(len(data_base[chat_id])):
                answer += f'{i + 1}) {data_base[chat_id][i]}\n'
            return answer
    elif text.startswith('бот добавь') or text.startswith('+'):
        if text.startswith('бот добавь'):
            start_split = 2
        else:
            start_split = 1
        if chat_id not in data_base:
            data_base[chat_id] = []
        for word in text.split()[start_split:]:
            answer += word + ' '
        data_base[chat_id].append(answer.strip())
        answer += 'добавлено'
        save()
    elif text.startswith('бот удали') or text.startswith('-'):
        if text.startswith('бот удали'):
            number = int(text.split()[2]) - 1
        else:
            number = int(text.split()[1]) - 1
        if len(data_base[chat_id]) > number:
            answer += data_base[chat_id][number]
            data_base[chat_id].pop(number)
            if not data_base[chat_id]:
                data_base.pop(chat_id)
            answer += ' удалено'
            save()
        else:
            return f'Элемента №{number + 1} нет'
    else:
        return ''

    return answer


if __name__ == '__main__':
    save()
    bot.polling()
