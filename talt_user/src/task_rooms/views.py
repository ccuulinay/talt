from flask_restplus import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from src import api
from src.task_rooms.models import state_parser, room_request, room_response
from src.task_rooms.service import TaskRoomService
from src.common.models import auth_parser
from flask_jwt_extended import get_jwt_identity

taskrooms_ns = Namespace('task_room', description="Task Room operations")
taskroom_service = TaskRoomService()

@taskrooms_ns.expect(auth_parser)
@taskrooms_ns.route("")
class Room(Resource):
    """
    Create and Get Rooms
    """
    @jwt_required
    @taskrooms_ns.expect(room_request)
    def post(self):
        """
        Create A room
        :return:
        """
        email = get_jwt_identity()
        payload = api.payload
        payload['users'] = [email]
        taskroom_service.create_room(payload)
        return {'Message': "Room created Successfully"}

    @jwt_required
    @taskrooms_ns.expect(state_parser)
    def get(self):
        """
        Get Active, Archived and Deleted Rooms
        :return:
        """
        email = get_jwt_identity()
        args = state_parser.parse_args()
        if self.validate_state(args['State']):
            response = taskroom_service.get_rooms(email, state=args['State'])
            return {'Message': "Rooms rendered successfully", 'records': marshal(response, room_response)}
        else:
            return {"Message": "State is not in (active|archived|deleted)"}

    @staticmethod
    def validate_state(state):
        if state == 'active' or state == 'archived' or state == 'deleted':
            return True
        else:
            return False


@taskrooms_ns.expect(auth_parser)
@taskrooms_ns.route('/<string:id>')
class RoomOperations(Resource):
    """
    Edit and Delete Rooms
    """
    @jwt_required
    @taskrooms_ns.expect(room_request)
    def put(self, id):
        """
        Edit a Room Name
        :param id:
        :return:
        """
        payload = api.payload
        taskroom_service.update_room(id, payload)
        return {'Message': "Room updated Successfully"}


@taskrooms_ns.expect(auth_parser)
@taskrooms_ns.route('/delete/<string:id>')
class RoomOperations(Resource):
    """
    Delete Rooms
    """
    @jwt_required
    def delete(self, id):
        """
        Delete Room
        :param id:
        :return:
        """
        taskroom_service.delete_room(id)
        return {'Message': "Room deleted successfully"}


@taskrooms_ns.expect(auth_parser)
@taskrooms_ns.route('/archive/<string:id>')
class RoomOperations(Resource):
    """
    Archive a room
    """
    @jwt_required
    def put(self, id):
        """
        Archive a Room Name
        :param id:
        :return:
        """
        taskroom_service.archive_room(id)
        return {'Message': "Room archived successfully"}


@taskrooms_ns.expect(auth_parser)
@taskrooms_ns.route('/undo/<string:id>')
class RoomOperations(Resource):
    """
    Move Rooms to Active Status
    """
    @jwt_required
    def put(self, id):
        """
        Move Rooms to Active Status
        :param id:
        :return:
        """
        taskroom_service.change_status(id)
        return {'Message': "Room status changed to Active"}