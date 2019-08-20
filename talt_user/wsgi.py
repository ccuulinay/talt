from src import application, api
from src.users.views import users_ns
from src.auth.views import auth_ns
from src.task_rooms.views import taskrooms_ns

api.add_namespace(users_ns, '/api/v1/users')
api.add_namespace(auth_ns, "/api/v1/auth")
api.add_namespace(taskrooms_ns, "/api/v1/task_rooms")

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=31865)
