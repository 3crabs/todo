class Chat:

    def __init__(self, chat_id: str, chat_list: list = None):
        if chat_list is None:
            chat_list = []
        self.id = chat_id
        self.chat_list = chat_list
