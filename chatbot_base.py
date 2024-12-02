"""
Base Chatbot class

"""

class ChatbotBase:
    # Initializes the chatbot with a name and active status.
    def __init__(self, name="Chatbot"):
        self.name = name
        self.conversation_is_active = True  # Keeps track of whether the chatbot is still active.

    # Greeting message.
    def greeting(self):
        print(f'Hello I am {self.name}')

    # Goodbye message.
    def farewell(self):
        print('Goodbye!')

    