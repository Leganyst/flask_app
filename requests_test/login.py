import requests

# Базовый URL
base_url = "http://localhost:5000"

# Регистрация пользователя и получение токена
auth_url = f"{base_url}/auth"
auth_data = {"username": "admin", "password": "admin_password"}
auth_response = requests.post(auth_url, json=auth_data)
access_token = auth_response.json().get("access_token", "")

# Запрос информации о студенте (требует токен)
student_url = f"{base_url}/students/1"
headers_with_token = {"Authorization": f"Bearer {access_token}"}
student_response = requests.get(student_url, headers=headers_with_token)

# Запрос информации о студенте без токена (должен вернуть ошибку)
student_unauthorized_response = requests.get(student_url)

# Попытка аутентификации с неверными учетными данными (должен вернуть ошибку)
wrong_auth_data = {"username": "admin", "password": "wrong_password"}
wrong_auth_response = requests.post(auth_url, json=wrong_auth_data)

# Вывод результатов
print("Auth Response:", auth_response.json())
print("Student Response (with Token):", student_response.json())
print("Student Unauthorized Response:", student_unauthorized_response.json())
print("Wrong Auth Response:", wrong_auth_response.json())
