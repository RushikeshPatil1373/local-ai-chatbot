from .services import ChatbotService

chatbot = ChatbotService()

while True:
    input_text = input("Enter your prompt: ")
    if input_text.lower() == "exit":
        break
    response = chatbot.ask(input_text)
    print(response)