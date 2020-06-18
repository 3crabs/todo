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
        if text.startswith('++'):
            text = text.replace('++', '').strip()
            self.get_chat_by_id(chat_id).chat_list.append(ListItem(text))
            return f'{text}', None

        if text == '??':
            text = ''
            for i in range(len(self.get_chat_by_id(chat_id).chat_list)):
                item = self.get_chat_by_id(chat_id).chat_list[i]
                text += f'{i + 1}) {item.label}'
                if item.state == 'strike':
                    text = f'<strike>{text}</strike>'
            if text == '':
                return 'Список пуст', None
            return f'{text}', None

        if text.startswith('**'):
            self.get_chat_by_id(chat_id).chat_list[0].state = 'strike'
            return self.get_chat_by_id(chat_id).chat_list[0].label, None
