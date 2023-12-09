from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from config import app_flask, api, jwt


# "База данных" в памяти для студентов
students_db = {
    1: {'id': 1, 'name': 'John Doe', 'age': 20},
    2: {'id': 2, 'name': 'Jane Smith', 'age': 22},
    3: {'id': 3, 'name': 'Bob Johnson', 'age': 21},
}

# Пример пользователей (в реальном проекте следует использовать хешированные пароли)
users = {
    'admin': {'password': 'admin_password'},
    'user1': {'password': 'user1_password'},
}


# Метод для генерации JWT токена при успешной аутентификации
def authenticate(username, password):
    if username in users and users[username]['password'] == password:
        access_token = create_access_token(identity=username)
        return make_response(jsonify(access_token=access_token), 200)
    else:
        return make_response(jsonify({'error': 'Invalid credentials'}), 401)


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
    @jwt_required()  # Этот декоратор требует валидный JWT токен для доступа к ресурсу
    def get(self, student_id):
        # Получаем идентификатор текущего пользователя из токена
        current_user = get_jwt_identity()

        # Проверяем, есть ли студент с указанным идентификатором
        if student_id in students_db:
            student = students_db[student_id]
            return make_response(jsonify(student), 200)
        else:
            return make_response(jsonify({'error': 'Student not found'}), 404)

# Регистрируем ресурсы
api.add_resource(StudentResource, '/students/<int:student_id>')
