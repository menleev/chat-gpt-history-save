from ChatGPT_SQL import ChatGPTurbo

if __name__ == "__main__":
    while True:
        print("Введите ник")
        name = input()
        print("Введите вопрос")
        message = input()
        print(ChatGPTurbo.chater(name, message))
