from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token
from flask import make_response, jsonify

from app.models import users, students_db

# Метод для генерации JWT токена при успешной аутентификации
def authenticate(username, password):
    if username in users and users[username]['password'] == password:
        # Создаем access token и refresh token
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        # Возвращаем оба токена в ответе
        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token), 200)
    else:
        return make_response(jsonify({'error': 'Invalid credentials'}), 401)


# Метод для обновления токена
def refresh_token():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return make_response(jsonify(access_token=new_token), 200)
