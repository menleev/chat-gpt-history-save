import openai
import re
import sqlite3

#user - передает индификатор пользователя
#message - передает сообщение пользователя

class ChatGPTurbo():
    def __init__(self):
        openai.api_key = "ВАШ КЛЮЧ"
    
    #главная функция
    def chater(self, user, message):
        #создаем таблицу chatgpt.db
        while True:
            try:
                if user[0].isdigit(): #проверяем на наличие цифры в начале имени
                    user = "_" + user #если нашло то добавляем символ
                length = len(message) #получаем колличество символов в отправленном сообщении
                if length >= 4000: #если в отправленном сообщение от пользователя (от вас) символов больше 4к 
                    return "Вы превысили лимит в 4000 символах за 1 смс" #возвращаем ошибку
                return self.response(self.update_db(user, "user", message), self.give_result(user)) #каша но да похер, за то уместил всё)))
            except openai.error.AuthenticationError: #если ошибка в ключе то возвращаем ошибку
                return "Ошибка в ключе активации OPENAI"
            except openai.error.InvalidRequestError: #если ошибка в превышения лимита символов в истории запросов пользователя
                self.delete_info_db(user)
                continue
            except Exception as e: #хз если ошибки будут логируйте (лучше использовать модуль Logger для отлова таких ошибок)
                return e
    
    #отправляем запрос чтобы получить ответ от бота
    def response(self, user, data):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=data
        )
        self.update_db(user, "assistant", re.sub(r'[^\w\s]', '', response['choices'][0]['message']['content']))
        return response['choices'][0]['message']['content']
    
    #очищаем таблицу в случае превышения лимит в символах от пользователя
    def delete_info_db(self, user):
        db = sqlite3.connect("chatgpt.db")
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM {user} WHERE role = 'user' or role = 'assistant'")
        db.commit()
        db.close()
    
    #получаем полную историю пользователя для коректного ответа и с сохранием истории для продолжения/дописания нужного
    def give_result(self, user):
        db = sqlite3.connect("chatgpt.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {user}")
        data = cursor.fetchall()
        db.close()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in data]
        return data
    
    #обновление или добавления пользователя и его данных + данных от бота в таблицу
    def update_db(self, user, role, message):
        db = sqlite3.connect("chatgpt.db")
        cursor = db.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {user} (role TEXT, content TEXT)")
        db.commit()
        cursor.execute(f"SELECT * FROM {user}")
        if cursor.fetchone() == None:
            cursor.execute(f"INSERT INTO {user} VALUES ('system', 'Helper')")
            db.commit()
        cursor.execute(f"INSERT INTO {user} VALUES ('{role}', '{message}')")
        db.commit()
        db.close()
        return user
    