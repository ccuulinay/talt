from flask_restplus import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from src import api, logger
from src.task_rooms.tasks.models import task_request, state_parser, task_response
from src.task_rooms.tasks.service import TasksService
from src.common.models import auth_parser

tasks_ns = Namespace('tasks', description="Task operations")
tasks_service = TasksService()


@tasks_ns.expect(auth_parser)
@tasks_ns.route('/<string:id>')
class Tasks(Resource):
    """
    Tasks Operations - Pass task room id as input
    """

    @tasks_ns.expect(state_parser)
    @jwt_required
    def get(self, id):
        """
        Get the tasks in the task room.
        :param id:
        :return:
        """
        args = state_parser.parse_args()
        if self.validate_state(args['State']):
            response = tasks_service.get_tasks(id, state=args['State'])
            logger.debug(response)
            return {'Message': "Rooms rendered successfully", 'records': marshal(response, task_response)}
        else:
            return {"Message": "State is not in (active|archived|deleted)"}

    @staticmethod
    def validate_state(state):
        if state == 'active' or state == 'archived' or state == 'deleted':
            return True
        else:
            return False


    @jwt_required
    @tasks_ns.expect(task_request)
    def post(self, id):
        """
        Add a Task to the Task Room
        :return:
        """
        payload = marshal(api.payload, task_request)
        tasks_service.create_task(id, payload)
        return {'status': "Task created successfully"}


@tasks_ns.expect(auth_parser)
@tasks_ns.route('/<string:taskroom_id>/<string:task_id>')
class Tasks(Resource):
    """
    Tasks Operations PUT - Pass task room id and task id as input
    """
    @jwt_required
    @tasks_ns.expect(task_request)
    def put(self, taskroom_id, task_id):
        """
        Edit a task with payload, given taskroom_id and task_id
        :param taskroom_id:
        :param task_id:
        :return:
        """
        payload = marshal(api.payload, task_request)
        tasks_service.update_task(taskroom_id, task_id, payload)
        return {'status': "Task updated successfully"}


@tasks_ns.expect(auth_parser)
@tasks_ns.route('/archive/<string:taskroom_id>/<string:task_id>')
class Tasks(Resource):
    """
    Tasks Operations Archive - Pass task room id and task id as input
    """
    @jwt_required
    def put(self, taskroom_id, task_id):
        """
        Archive a task
        :param taskroom_id:
        :param task_id:
        :return:
        """
        tasks_service.archive_task(taskroom_id, task_id)
        return {'status': "Task archived successfully"}


@tasks_ns.expect(auth_parser)
@tasks_ns.route('/delete/<string:taskroom_id>/<string:task_id>')
class Tasks(Resource):
    """
    Tasks Operations Delete - Pass task room id and task id as input
    """

    @jwt_required
    def delete(self, taskroom_id, task_id):
        """
        Delete a taks
        :param taskroom_id:
        :param task_id:
        :return:
        """
        tasks_service.delete_task(taskroom_id, task_id)
        return {'status': "Task deleted successfully"}


@tasks_ns.expect(auth_parser)
@tasks_ns.route('/undo/<string:taskroom_id>/<string:task_id>')
class Tasks(Resource):
    """
    Tasks Operations Undo Delete/Archive - Pass task room id and task id as input
    """

    @jwt_required
    def put(self, taskroom_id, task_id):
        """

        :param taskroom_id:
        :param task_id:
        :return:
        """
        tasks_service.undo_task(taskroom_id, task_id)
        return {'status': "Task activated successfully"}
