import json
import random

class ChatBot:
    def __init__(self, intents_file):
        with open(intents_file) as file:
            self.intents = json.load(file)['intents']
    
    def get_response(self, user_input):
        user_input = user_input.lower()
        
        for intent in self.intents:
            for pattern in intent['patterns']:
                if user_input in pattern.lower():
                    return random.choice(intent['responses'])
        
        return "I'm not sure how to respond to that. Try asking something else."

def main():
    print("ChatBot: Hello! I'm your friendly chatbot. Type 'quit' to exit.")
    chatbot = ChatBot('intents.json')
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("ChatBot: Goodbye!")
            break
        
        response = chatbot.get_response(user_input)
        print(f"ChatBot: {response}")

if __name__ == "__main__":
    main()