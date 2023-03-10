from ChatGPT import ChatGPTurbo

def che():
    chat = ChatGPTurbo()
    while True:
        print("Введите ник")
        name = input()
        #Введите вопрос
        print("Введите вопрос")
        message = input()
        res = chat.chater(name, message)
        print(res)
        
if __name__ == "__main__":
    che()