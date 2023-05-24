import requests

url = 'http://localhost:8081'  # Адрес вашего приложения

# Пример данных, которые вы хотите отправить
data = {
    'param1': 'value1',
    'param2': 'value2'
}

response = requests.post(url, data=data)
print(response.text)  # Вывод ответа от сервера
response2 = requests.get(url, data=data)
print(response2.text)
