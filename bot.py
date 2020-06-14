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

data_base = []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет я todo bot от 3CRABS soft!\n"
                                      "Чтобы узнать подробности введи /help")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Я пока ничего не умею(")


@bot.message_handler(content_types=["text"])
def content_text(message):
    bot.send_message(message.chat.id, message.text)


def content_text_answer(text: str) -> str:
    answer = ''

    if text == 'бот покажи список':
        if data_base:
            answer += 'Ваш список\n'
            for i in range(len(data_base)):
                answer += f'{i+1}) {data_base[i]}\n'
            return answer
        return 'Ваш список пока пуст'
    elif 'добавь' in text:
        for word in text.split()[2:]:
            answer += word + ' '
        data_base.append(answer)
        answer += 'добавлено'
    else:
        number = int(text.split()[2]) - 1
        answer += data_base[number]
        data_base.remove(data_base[0])
        answer += 'удалено'

    return answer


if __name__ == '__main__':
    bot.polling()
