class Message:
    text = ""
    chatId = ""
    updateId = ""
    def __init__(self, text, chatId, updateId):
        self.text = text
        self.chatId = chatId
        self.updateId = updateId