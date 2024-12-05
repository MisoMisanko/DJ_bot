"""
Base Chatbot class

"""

class ChatbotBase:
    def __init__(self, name="Chatbot"):
        self.name = name
        self.conversation_is_active = True

    def greeting(self):
        print(f'Hello I am {self.name}')

    def farewell(self):
        print('Goodbye!')

    