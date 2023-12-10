from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from config import app_flask, api, jwt
from app.models import users, students_db

from app.utils.jwt_token import authenticate


# Ресурс для аутентификации
class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        return authenticate(username, password)

# Регистрируем ресурсы для аутентификации
api.add_resource(AuthResource, '/auth')


# Ресурс для работы со студентами
class StudentResource(Resource):
    @jwt_required()  
    def get(self, student_id):
        # Получаем идентификатор текущего пользователя из токена
        current_user = get_jwt_identity()

        # Проверяем, есть ли студент с указанным идентификатором
        if student_id in students_db:
            student = students_db[student_id]
            return make_response(jsonify(student), 200)
        else:
            return make_response(jsonify({'error': 'Student not found'}), 404)


# Создаем URL для обновления токена
class TokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # Получаем идентификатор пользователя из refresh token
        current_user = get_jwt_identity()
        # Создаем новый access token
        new_token = create_access_token(identity=current_user)
        # Возвращаем новый access token в ответе
        return make_response({'access_token': new_token}, 200)

# Регистрируем ресурсы
api.add_resource(StudentResource, '/students/<int:student_id>')
api.add_resource(TokenRefreshResource, '/refresh_token')


