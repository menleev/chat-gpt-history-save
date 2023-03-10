from ChatGPT import ChatGPTurbo

def che():
    chat = ChatGPTurbo()
    while True:
        print("Введите ник")
        name = input()
        #Введите вопрос
        print("Введите вопрос")
        question = input()
        res = chat.chater(name, question)
        print(res)
        
if __name__ == "__main__":
    che()