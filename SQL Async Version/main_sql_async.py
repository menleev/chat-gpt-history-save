import asyncio
from ChatGPT_SQL_ASYNC import ChatGPTurbo

if __name__ == "__main__":
    while True:
        loop = asyncio.new_event_loop()
        print("Введите ник")
        name = input()
        print("Введите вопрос")
        message = input()
        try:
            print(loop.run_until_complete(ChatGPTurbo().chater(f'{name}', f'{message}')))
        except Exception as e:
            print(e)