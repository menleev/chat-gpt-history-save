import openai
import re
import sqlite3


class ChatGPTurbo():
    def __init__(self):
        openai.api_key = "ВАШ КЛЮЧ"
    
    #главная функция
    def chater(self, user, message):
        if user[0].isdigit(): #проверяем на наличие цифры в начале имени
            user = "_" + user #если нашло то добавляем символ
        length = len(message) #получаем колличество символов в отправленном сообщении
        if length >= 4000: #если в отправленном сообщение от пользователя (от вас) символов больше 4к 
            return "Вы превысили лимит в 4000 символах за 1 смс" #возвращаем ошибку
        self.check_file_db(user) #проверяем наличие имени в базе данных
        self.update_system_db(user) #записываем в базу данных имя пользователя
        self.update_user_db(user, message) #записываем в базу данных имя пользователя и сообщение
        repl = self.give_result(user) #получаем сконвертированный ответ
        try:
            resp = self.response(user, repl) #отправляем запрос
            return resp #получаем ответ
        except openai.error.AuthenticationError: #если ошибка в ключе то возвращаем ошибку
            return "Ошибка в ключе активации OPENAI"
        except Exception as e:
            self.delete_info_db(user) #если превышен лимит символов 4000 в истории сообщений юзера то он очистит базу данных данного юзера и ответов бота
            self.chater(user, message) #начинаем с начала чтобы не терять вопрос
    
    #получаем текущий путь и проверяем
    def check_file_db(self, user):
        db = sqlite3.connect("chatgpt.db")
        cursor = db.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {user} (role TEXT, content TEXT)")
        db.commit()
        db.close()
    
    #получаем результат форматирования
    def give_result(self, user):
        conn = sqlite3.connect("chatgpt.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {user}")
        data = cursor.fetchall()
        conn.close()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in data]
        return data
    
    #отправляем запрос
    def response(self, user, resp):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=resp
        )
        reply = response.choices[0].message.content
        paraha = re.sub(r'[^\w\s]', '', reply)
        self.update_assistant_db(user, paraha)
        return reply
    
    #функция очистки таблицы
    def delete_info_db(self, user):
        conn = sqlite3.connect("chatgpt.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {user} WHERE role = 'user' or role = 'assistant'")
        conn.commit()
        conn.close()
        print("Информация удалена")
    
    #читаем из базы данных
    def ready_db(self, user):
        db = sqlite3.connect("chatgpt.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM {}".format(user))
        data = cursor.fetchall()
        db.close()
        return data
    
    #обновляем информацию system в json
    def update_system_db(self, user):
        db = sqlite3.connect("chatgpt.db")
        cursor = db.cursor()
        data = self.ready_db(user)
        if len(data) == 0:
            cursor.execute(f"INSERT INTO {user} VALUES ('system', 'HELPER')")
            db.commit()
            db.close()
        else:
            return
        
    #обновляем информацию assistant в json
    def update_assistant_db(self, user, reply):
        db = sqlite3.connect("chatgpt.db")
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO {user} VALUES ('assistant', '{reply}')")
        db.commit()
        db.close()

    
    #обновляем информацию user в json
    def update_user_db(self, user, message):
        db = sqlite3.connect("chatgpt.db")
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO {user} VALUES ('user', '{message}')")
        db.commit()
        db.close()