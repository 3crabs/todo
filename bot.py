import json

import telebot

configFileName = 'telegram_token.json'
try:
    with open(configFileName, 'r') as file:
        data = file.read()
except FileNotFoundError as e:
    print(f"File {configFileName} not found.")
    exit()
config = json.loads(data)

bot = telebot.TeleBot(config["token"])

data_base = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет я todo bot от 3CRABS soft!\n"
                                      "Чтобы узнать подробности введи /help")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Напиши:\n"
                                      "бот добавь {название пункта}\n"
                                      "бот покажи список\n"
                                      "бот удали {номер пункта}")


@bot.message_handler(content_types=["text"])
def content_text(message):
    answer = content_text_answer(message.text.lower(), message.chat.id)
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
    elif 'удали' in text:
        number = int(text.split()[2]) - 1
        answer += data_base[chat_id][number]
        data_base[chat_id].pop(0)
        if not data_base[chat_id]:
            data_base.pop(chat_id)
        answer += ' удалено'
    else:
        return ''

    return answer


if __name__ == '__main__':
    bot.polling()
