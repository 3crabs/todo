from src.ListItem import ListItem


class TodoBot:

    def __init__(self):
        self.lists = {}

    def get_list(self, chat_id: str):
        if chat_id in self.lists:
            return self.lists[chat_id]['list']
        else:
            return None

    def content_text_answer(self, text: str, chat_id: str):
        if chat_id not in self.lists:
            self.lists[chat_id] = {'list': []}

        if text.startswith('++'):
            text = text.replace('++', '').strip()
            self.get_list(chat_id).append(ListItem(text))
            return f'{text}', None

        if text == '??':
            text = ''
            for i in range(len(self.get_list(chat_id))):
                item = self.get_list(chat_id)[i]
                text += f'{i + 1}) {item.label}'
                if item.state == 'strike':
                    text = f'<strike>{text}</strike>'
            return f'{text}', None

        if text.startswith('**'):
            self.get_list(chat_id)[0].state = 'strike'
            return self.get_list(chat_id)[0].label, None
