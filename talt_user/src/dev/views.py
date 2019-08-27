from flask_restplus import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.common.models import auth_parser

dev_ns = Namespace('tasks', description="Task operations")


@dev_ns.expect(auth_parser)
@dev_ns.route('')
class Dev(Resource):
    """
    Dev operations for learning
    """

    @jwt_required
    def get(self):
        email = get_jwt_identity()
        msg = {"Message": "Welcome " + email}
        return msg
