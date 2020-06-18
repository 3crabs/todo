from src.Chat import Chat
from src.ListItem import ListItem


class TodoBot:

    def __init__(self):
        self.chats = []

    def get_chat_by_id(self, chat_id: str):
        for chat in self.chats:
            if chat.id == chat_id:
                return chat
        chat = Chat(chat_id)
        self.chats.append(chat)
        return chat

    def content_text_answer(self, text: str, chat_id: str):
        text = text.strip()

        if text.startswith('++'):
            text = text.replace('++', '').strip()
            self.get_chat_by_id(chat_id).chat_list.append(ListItem(text))
            return f'Добавлено: "{text}"', None

        if text == '??':
            answer = ''
            for i in range(len(self.get_chat_by_id(chat_id).chat_list)):
                item = self.get_chat_by_id(chat_id).chat_list[i]
                text = f'{i + 1}) {item.label}'
                if item.state == 'strike':
                    text = f'<strike>{text}</strike>'
                text += '\n'
                answer += text
            if answer == '':
                return 'Список пуст', None
            return f'Ваш список:\n{answer}', None

        if text.startswith('**'):
            i = int(text.replace('**', '').strip()) - 1
            self.get_chat_by_id(chat_id).chat_list[i].state = 'strike'
            text = self.get_chat_by_id(chat_id).chat_list[i].label
            return f'Зачеркнуто: "{text}"', None

        if text == '---':
            chat_list = self.get_chat_by_id(chat_id).chat_list
            len_chat_list = len(chat_list)
            for i in range(len_chat_list):
                k = len_chat_list - i - 1
                if chat_list[k].state == 'strike':
                    chat_list.pop(k)
            return 'Все зачеркнутые дела удалены', None

        if text.startswith('--'):
            i = int(text.replace('--', '').strip()) - 1
            item = self.get_chat_by_id(chat_id).chat_list.pop(i)
            text = item.label
            return f'Зачеркнуто: "{text}"', None
