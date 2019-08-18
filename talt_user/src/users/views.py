from flask  import request
from flask_restplus import Namespace, Resource
from src import api
from src.users.models import user_request, user, user_base
from src.users.service import UserService

users_ns = Namespace('users', description='User Management')
user_service = UserService()


@users_ns.route('')
class Users(Resource):
    '''
    Add Users
    '''
    @users_ns.expect(user_request)
    def post(self):
        """

        :return:
        """
        user_service.signup(api.payload)
        return {'status': 'Signed up Successfully', 'status_code': 200}


@users_ns.route('/activate/<string:id>')
class UserActivate(Resource):
    """
    Activate User
    """
    def get(self, id):
        """
        Activate ther User
        :param id:
        :return:
        """
        user_service.activate(id)
        return {'status': "User Activated Successfully", 'status_code': 200}

