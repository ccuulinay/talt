from bson import ObjectId
from src.task_rooms.models import room_request, room_record
from src.utils.mongodb_utils import MongoBase as Base
from src.utils.helper import custom_marshal, update_common_payload
from src.common.constants import COLLECTIONS

base_obj = Base()

class TaskRoomService(object):
    """
    Service class for Tasks & Rooms View
    """
    def create_room(self, payload):
        """
        Create room for users
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, room_record, "create")
        _id = base_obj.insert(COLLECTIONS['ROOMS'], payload)

    def get_rooms(self, email, state):
        """
        Get Rooms for a particular User
        :param email:
        :param state:
        :return:
        """
        if state == 'active':
            query = {"users": email, "meta.is_deleted": False, "meta.is_archived": False}
        elif state == 'archived':
            query = {"users": email, "meta.is_archived": True}
        elif state == 'deleted':
            query = {"users": email, "meta.is_deleted": True}

        count, records = base_obj.get(COLLECTIONS['ROOMS'], query)
        return records

    def update_room(self, id, payload):
        """
        Update Room
        :param id:
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, room_request, 'update')
        base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id)}, {"$set": payload})

    def archive_room(self, id):
        """
        Archive Room
        :param id:
        :return:
        """
        payload = update_common_payload()
        payload["meta.is_archived"], payload["meta.is_deleted"] = True, False
        base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id)},
                        {"$set": payload})

    def delete_room(self, id):
        """
        Delete Room
        :param id:
        :return:
        """
        payload = update_common_payload()
        payload["meta.is_archived"], payload["meta.is_deleted"] = False, True
        base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id)},
                        {"$set": payload})

    def change_status(self, id):
        """
        Change Status to Active
        :param id:
        :return:
        """
        payload = update_common_payload()
        payload["meta.is_archived"], payload["meta.is_deleted"] = False, False
        base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id)},
                        {"$set": payload})
