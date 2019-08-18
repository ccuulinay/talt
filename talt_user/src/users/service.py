from flask import abort
from bson import ObjectId
from passlib.hash import sha256_crypt
from src.users.models import user
from src.utils.mongodb_utils import MongoBase as Base
from src.utils.mail_utils import send_mail
from src.utils.helper import custom_marshal
from src.common.constants import COLLECTIONS, ACTIVATION_MAIL
from src import logger

base_obj = Base()


class UserService(object):
    """
    Service Class for User View
    """
    def signup(self, payload):
        """
        signup function
        :return:
        """
        if payload.get('password') != payload.get('confirm_password'):
            abort(400, "Password does not match")
        count, records = base_obj.get(COLLECTIONS['USERS'], {"email_addr": payload['email_addr']})
        if count > 0:
            abort(400, "Email ID Already Exists")
        payload = custom_marshal(payload, user, 'create')
        payload['password'] = sha256_crypt.encrypt(payload['password'])
        _id = base_obj.insert(COLLECTIONS['USERS'], payload)
        logger.debug("{}, {}".format(str(_id), type(_id)))
        link = ACTIVATION_MAIL.format(id=_id)
        logger.debug(link)
        send_mail([payload['email_addr']],"Todo App Account Activation", link, 'signup.html', {'link': link, 'name': payload['first_name']})

    def activate(self, id):
        """
        Activate the user
        :param id:
        :return:
        """
        count, records = base_obj.get(COLLECTIONS['USERS'], {"_id": ObjectId(id)})
        if count == 0:
            abort(400, "Invalid Link")
        if records[0]['is_active']:
            abort(400, "Account Already Active")
        else:
            base_obj.update(COLLECTIONS['USERS'], {"_id": ObjectId(id)}, {"$set": {"is_active": True}})