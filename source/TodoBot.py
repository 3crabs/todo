from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from source.models.Base import Base
from source.models.Item import Item
from source.models.ItemState import ItemState
from source.models.List import List


class TodoBot:

    def __init__(self, database_name: str):
        self.database_name = database_name
        engine = create_engine(database_name)
        Base.metadata.create_all(engine)

    def get_session(self):
        engine = create_engine(self.database_name)
        return sessionmaker(bind=engine)()

    def message_handler(self, text: str, chat_id: str) -> str:
        if text == '++' or text == '--' or text == '—' or text == '**':
            return ''

        if text == '---' or text == '—-':
            return self.delete_all(chat_id)
        if text == '--*':
            return self.delete_all_mark(chat_id)
        elif text.startswith('++'):
            return self.add_item(chat_id, text.replace('++', '').strip())
        elif text.startswith('**'):
            return self.mark_item(chat_id, text.replace('**', '').strip())
        elif text.startswith('--') or text.startswith('—'):
            return self.delete_item(chat_id, text.replace('—', '--').replace('--', '').strip())
        elif text == '??':
            return self.get_list(chat_id)

    def delete_all(self, chat_id):
        session = self.get_session()
        list = session.query(List).filter_by(chat_id=chat_id).first()
        if list:
            items = session.query(Item).filter_by(list_id=list.id).all()
            for item in items:
                item.state = ItemState.DELETE
            session.commit()
        return 'Все элементы удалены'

    def delete_all_mark(self, chat_id):
        session = self.get_session()
        list = session.query(List).filter_by(chat_id=chat_id).first()
        if list:
            items = session.query(Item).filter_by(list_id=list.id, state=ItemState.MARK).all()
            for item in items:
                item.state = ItemState.DELETE
            session.commit()
        return 'Все зачеркнутые элементы удалены'

    def add_item(self, chat_id, text):
        session = self.get_session()
        list = session.query(List).filter_by(chat_id=chat_id).first()
        if list is None:
            list = List(chat_id)
        session.add(Item(text, list))
        session.commit()
        return f'Добавлено "{text}"'

    def mark_item(self, chat_id, text):
        try:
            number = int(text) - 1
        except ValueError:
            return f'"{text}" непохоже на номер в списке'
        session = self.get_session()
        list = session.query(List).filter_by(chat_id=chat_id).first()
        items = session.query(Item).filter(Item.list == list, Item.state != ItemState.DELETE).all()
        if number >= len(items):
            return f'Элемента с номером {number + 1} нет в вашем списке'
        if number < 0:
            return f'Элемента с номером {number + 1} не может быть в вашем списке'
        items[number].state = ItemState.MARK
        session.commit()
        return f'Зачеркнуто "{items[number].name}"'

    def get_list(self, chat_id):
        session = self.get_session()
        list = session.query(List).filter_by(chat_id=chat_id).first()
        items = session.query(Item).filter(Item.list == list, Item.state != ItemState.DELETE).all()
        if not items:
            return 'Список пуст'
        answer = ''
        for i in range(len(items)):
            if items[i].state == ItemState.MARK:
                answer += f'<strike>{i + 1}) {items[i].name}</strike>'
            else:
                answer += f'{i + 1}) {items[i].name}'
            if i < len(items) - 1:
                answer += '\n'
        return answer

    def delete_item(self, chat_id, text):
        try:
            number = int(text) - 1
        except ValueError:
            return f'"{text}" непохоже на номер в списке'
        session = self.get_session()
        list = session.query(List).filter_by(chat_id=chat_id).first()
        items = session.query(Item).filter(Item.list == list, Item.state != ItemState.DELETE).all()
        if number >= len(items):
            return f'Элемента с номером {number + 1} нет в вашем списке'
        if number < 0:
            return f'Элемента с номером {number + 1} не может быть в вашем списке'
        items[number].state = ItemState.DELETE
        session.commit()
        return f'Удалено "{items[number].name}"'
