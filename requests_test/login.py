import requests
from time import sleep

def login(username, password):
    auth_url = "http://localhost:5000/auth"
    auth_data = {"username": username, "password": password}
    response = requests.post(auth_url, json=auth_data)
    # Получаем access token и refresh token из ответа
    access_token = response.json().get("access_token", "")
    refresh_token = response.json().get("refresh_token", "")
    # Возвращаем оба токена
    return access_token, refresh_token


def get_student_info(student_id, access_token):
    student_url = f"http://localhost:5000/students/{student_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(student_url, headers=headers)
    return response.json()

def refresh_token(refresh_token_str):
    # Используем правильный URL, метод и тип токена
    refresh_url = "http://localhost:5000/refresh_token"
    headers = {"Authorization": f"Bearer {refresh_token_str}"}
    response = requests.post(refresh_url, headers=headers)
    return response.json().get("access_token", "")

# Логинимся и получаем токен
access_token, refresh_token_str = login("admin", "admin_password")
print("Initial Token:", access_token)
print("Refresh Token:", refresh_token_str)

sleep(10)

  # Пытаемся сделать запрос с текущим токеном
student_info = get_student_info(1, access_token)
print("Student Info:", student_info)

status = student_info.get('msg')
if status == "Token has expired":
    # Обновляем токен с помощью refresh token
    new_access_token = refresh_token(refresh_token_str)
    print("New Token:", new_access_token)
    # Повторяем запрос с новым токеном
    student_info = get_student_info(1, new_access_token)
    print("Student Info:", student_info)
