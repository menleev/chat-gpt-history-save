import os
import openai
import json

class ChatGPTurbo():
    def __init__(self):
        openai.api_key = "ВАШ КЛЮЧ"
    
    #главная функция
    def chater(self, user, message):
        while True:
            self.check_file_json(user) #проверяем наличия файла
            self.check_json(user) #проверяем на лимит символов json
            resp = self.update_user_json(user, message) #записываем в json наш вопрос
            reply = self.response(resp, user) #получаем ответ
            if reply == False:
                continue
            return reply #возвращаем ответ
    
    #отправляем запрос
    def response(self, resp, user):
        print(resp)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=resp
            )
            reply = response.choices[0].message.content
            reply = self.update_assistant_json(user, reply)
            return reply
        except Exception as e:
            self.delete_json(user)
            return False
            
    #получаем текущий путь и проверяем
    def check_file_json(self, user):
        if not os.path.exists("chatgpt"):
            os.mkdir("chatgpt")
        if not os.path.exists(f"chatgpt\\{user}.json"):
            self.update_system_json(user)
        return True
    
    #читаем из json
    def ready_json(self, user):
        with open(f"chatgpt\\{user}.json", "r") as f:
            data = json.load(f)
        return data
    
    #удаляем из json
    def delete_json(self, user):
        with open(f"chatgpt\\{user}.json", "r") as f:
            users = json.load(f)
            users.pop(0)
            with open(f"chatgpt\\{user}.json", "w") as f:
                json.dump([{'role': "system", "content": "You are a helpful and kind AI Assistant."}], f, indent=4)
    
    #проверяем наличие лимита символов в user запросах (макс 4к)
    def check_json(self, user):
        data = self.ready_json(user)
        count = 0
        for ent in data:
            if ent['role'] == 'user':
                count += len(ent['content'])
        if count > 4000:
            self.delete_json(user)
        return True
    
    #обновляем информацию system в json
    def update_system_json(self, user):
        with open(f"chatgpt\\{user}.json", "w") as f:
            json.dump([{'role': "system", "content": "Helper."}], f, indent=4)
    
    #обновляем информацию assistant в json
    def update_assistant_json(self, user, reply):
        with open(f"chatgpt\\{user}.json", "r") as f:
            data = json.load(f)
            data.append({'role': "assistant", "content": reply})
            with open(f"chatgpt\\{user}.json", "w") as f:
                json.dump(data, f, indent=4)
        return reply
    
    #обновляем информацию user в json
    def update_user_json(self, user, message):
        with open(f"chatgpt\\{user}.json", "r") as f:
            users = json.load(f)
            users.append({"role": "user", "content": message})
            with open(f"chatgpt\\{user}.json", "w") as f:
                json.dump(users, f, indent=4)
        return users