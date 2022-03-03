import base64
import requests
from pprint import pprint
from datetime import datetime

# HOST = 'http://127.0.0.1:8000'

# #Регистрация нового пользователя
# response = requests.post(f'{HOST}/user', json={
#                                                 # 'first_name': 'Igor',
#                                               # 'last_name': 'Sverchkov',
#                                                'password': 'Privet11',
#                                                'email': 'b@mail.ru',
#                                                'user_login': 'Ivan'
#                                             }
#                          )


# #Получение токена
# secret_code = base64.b64encode(b"Ivan:Privet11").decode()
# response = requests.post(f'{HOST}/login', headers={"Authorization": f'basic {secret_code}'})
# token = response.json()['token']


# #Создание нового объявления
# response = requests.post(f'{HOST}/adv',
#                          headers = {'x-access-tokens': f'{token}'},
#                          json={'title': 'Продажа стула'}
#                          )


# #Получение конкретного объявления
# response = requests.get(f'{HOST}/adv/5',
#                          headers = {'x-access-tokens': f'{token2}'}
#                          )


# #Удаление объявления пользователя
# response = requests.delete(f'{HOST}/adv/10',
#                          headers = {'x-access-tokens': f'{token2}'}
#                          )


# #Изменение объявления пользователя
# response = requests.put(f'{HOST}/adv/7',
#                          headers = {'x-access-tokens': f'{token2}'},
#                         json = {'title': 'Продажа куклы'}
#                          )


# print(response.status_code)
# pprint(response.json())