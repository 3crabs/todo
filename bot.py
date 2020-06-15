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
    bot.send_message(message.chat.id, "Напиши:\n"
                                      "бот добавь {название пункта}\n"
                                      "бот покажи список\n"
                                      "бот удали {номер пункта}\n\n"
                                      "Или команды:\n"
                                      "/start - привет бот\n"
                                      "/help - помощь\n"
                                      "/list - список\n")


@bot.message_handler(commands=["list"])
def send_list(message):
    bot.send_message(message.chat.id, content_text_answer('бот покажи список', str(message.chat.id)))


@bot.message_handler(content_types=["text"])
def content_text(message):
    answer = content_text_answer(message.text.lower(), str(message.chat.id))
    if answer != '':
        bot.send_message(message.chat.id, answer)


def content_text_answer(text: str, chat_id: str) -> str:
    answer = ''

    if text == 'бот покажи список':
        if chat_id not in data_base:
            return 'Ваш список пока пуст'
        if data_base[chat_id]:
            answer += 'Ваш список\n'
            for i in range(len(data_base[chat_id])):
                answer += f'{i + 1}) {data_base[chat_id][i]}\n'
            return answer
    elif 'добавь' in text:
        if chat_id not in data_base:
            data_base[chat_id] = []
        for word in text.split()[2:]:
            answer += word + ' '
        data_base[chat_id].append(answer.strip())
        answer += 'добавлено'
        save()
    elif 'удали' in text:
        number = int(text.split()[2]) - 1
        answer += data_base[chat_id][number]
        data_base[chat_id].pop(number)
        if not data_base[chat_id]:
            data_base.pop(chat_id)
        answer += ' удалено'
        save()
    else:
        return ''

    return answer


if __name__ == '__main__':
    save()
    bot.polling()
