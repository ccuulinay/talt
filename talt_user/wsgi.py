from src import application, api
from src.users.views import users_ns

api.add_namespace(users_ns, '/api/v1/users')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=31865)
