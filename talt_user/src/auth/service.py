from flask_restplus import abort
from passlib.hash import sha256_crypt
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from src.utils.mongodb_utils import MongoBase as Base
from src.common.constants import COLLECTIONS
from src import redis_store, application

base_obj = Base()

class AuthService(object):
    """
    Auth Related Services
    """
    def login(self, payload):
        """
        Login Function to return access and refresh token
        :param payload:
        :return:
        """
        email, password = payload['email_addr'], payload['password']
        count, records = base_obj.get(COLLECTIONS['USERS'], {'email_addr': email, "meta.is_deleted": False})
        if count > 0:
            if sha256_crypt.verify(password, records[0]['password']):
                if records[0]['is_active'] is True:
                    access_token = create_access_token(identity=email)
                    refresh_token = create_refresh_token(identity=email)
                    access_jti = get_jti(encoded_token=access_token)
                    refresh_jti = get_jti(encoded_token=refresh_token)
                    redis_store.set(access_jti, 'false', application.config['JWT_ACCESS_TOKEN_EXPIRES'])
                    redis_store.set(refresh_jti, 'false', application.config['JWT_REFRESH_TOKEN_EXPIRES'])
                    return {'access_token': access_token, 'refresh_token': refresh_token}
                else:
                    abort(401, Message="User is not activated. Activate User to Login")
            else:
                abort(401, Message="Password is incorrect")
        else:
            abort(401, Message="Email does not exists")