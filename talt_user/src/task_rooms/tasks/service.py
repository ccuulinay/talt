from bson import ObjectId
from flask_jwt_extended import get_jwt_identity
from src.task_rooms.tasks.models import task_db_input, task_request
from src.utils.mongodb_utils import MongoBase as Base
from src.utils.helper import custom_marshal, update_common_payload
from src.common.constants import COLLECTIONS
from src import logger


base_obj = Base()


class TasksService(object):
    """
    Tasks Service
    """

    tasks_status_mapping = {
        "active": {"is_archived": False, "is_deleted": False}
        , "archived": {"is_archived": True, "is_deleted": False}
        , "deleted": {"is_archived": False, "is_deleted": True}
    }

    def create_task(self, id, payload):
        """
        Create a task in task room
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, task_db_input, 'create')
        payload['_id'] = ObjectId()
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(id)},
                                 {"$push": {'tasks': payload}})

    def update_task(self, taskroom_id, task_id, payload):
        """
        Update the task id with payload, all users under "users" can update tasks
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        email = get_jwt_identity()
        payload = custom_marshal(payload, task_request, 'update', prefix="tasks.$")
        result = base_obj.update(COLLECTIONS['ROOMS']
            , {'_id': ObjectId(taskroom_id), 'tasks._id':ObjectId(task_id), 'users': email}
            , {"$set": payload})
        logger.info("payload: {}, result: {}".format(payload, result))

    def archive_task(self, taskroom_id, task_id):
        """
        Archive the task with id
        :param taskroom_id:
        :param task_id:
        :return:
        """
        email = get_jwt_identity()
        payload = update_common_payload(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = True, False
        result = base_obj.update(COLLECTIONS['ROOMS']
            , {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id), 'users': email}
            , {"$set": payload})
        logger.info("payload: {}, result: {}".format(payload, result))

    def delete_task(self, taskroom_id, task_id):
        """
        Delete the task with id
        :param taskroom_id:
        :param task_id:
        :return:
        """
        email = get_jwt_identity()
        payload = update_common_payload(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = False, True
        result = base_obj.update(COLLECTIONS['ROOMS']
            , {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id), "users": email}
            , {"$set": payload})
        logger.info("payload: {}, result: {}".format(payload, result))

    def undo_task(self, taskroom_id, task_id):
        """
        Activate the task with id
        :param taskroom_id:
        :param task_id:
        :return:
        """
        email = get_jwt_identity()
        payload = update_common_payload(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = False, False
        result = base_obj.update(COLLECTIONS['ROOMS']
            , {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id), "users": email}
            , {"$set": payload})
        logger.info("payload: {}, result: {}".format(payload, result))

    def get_tasks(self, id, state):
        """
        Get Tasks list
        :param id:
        :param state:
        :return:
        """
        email = get_jwt_identity()
        cond = {"$and": [
            {"$eq": ["$$task.meta.is_archived", self.tasks_status_mapping[state]["is_archived"]]}
            , {"$eq": ["$$task.meta.is_deleted", self.tasks_status_mapping[state]["is_deleted"]]}
        ]}
        query = [{"$match": {"_id": ObjectId(id), "users": email}},
                 {"$project": {"tasks": {"$filter":
                                             {"input": "$tasks"
                                                 , "as": "task"
                                                 , "cond": cond}}}}]
        records = base_obj.aggregate(COLLECTIONS["ROOMS"], query)
        tasks = records[0]['tasks']
        return tasks



