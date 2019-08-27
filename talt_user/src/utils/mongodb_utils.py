import pymongo
from pymongo import MongoClient
from src import application, logger
import functools
import time

MAX_AUTO_RECONNECT_ATTEMPTS = 5


def reconnect(mongo_op_func):
    """Gracefully handle a reconnection event."""

    @functools.wraps(mongo_op_func)
    def wrapper(*args, **kwargs):
        for attempt in range(MAX_AUTO_RECONNECT_ATTEMPTS):
            try:
                return mongo_op_func(*args, **kwargs)
            except pymongo.errors.AutoReconnect as e:
                wait_t = 0.5 * pow(2, attempt)  # exponential back off
                logger.warning("PyMongo auto-reconnecting... %s. Waiting %.1f seconds.", str(e), wait_t)
                time.sleep(wait_t)

    return wrapper


class MongoBase(object):
    def __init__(self):
        mongo_conn = MongoClient(application.config['MONGO_URI'])
        self.mongo_db = mongo_conn[application.config['DB_NAME']]

    @reconnect
    def get(self, collection_name, query):
        try:
            cursor = self.mongo_db[collection_name].find(query)
            count = cursor.count()
            return count, list(cursor)
        except Exception as e:
            print('Exception while getting from MongoDB', e)
            logger.debug('Exception while getting from MongoDB as exception: {}'.format(e))

    @reconnect
    def insert(self, collection_name, documents):
        try:
            collection = self.mongo_db[collection_name]
            if isinstance(documents, list):
                _id = collection.insert_many(documents, ordered=False).inserted_ids
            else:
                _id = collection.insert_one(documents).inserted_id
            return _id
        except pymongo.errors.BulkWriteError:
            logger.warning('Duplicated records.')
        except Exception as e:
            print('Exception while inserting to MongoDB', e)
            logger.debug('Exception while inserting to MongoDB as exception: {}'.format(e))

    @reconnect
    def update(self, collection_name, query, value):
        try:
            if isinstance(value, list):
                self.mongo_db[collection_name].update_many(query, value)
            else:
                self.mongo_db[collection_name].update_one(query, value)
        except Exception as e:
            print('Exception while updating MongoDB', e)
            logger.debug('Exception while updating MongoDB as exception: {}'.format(e))

    @reconnect
    def delete(self, collection_name, query):
        try:
            self.mongo_db[collection_name].update_many(query, {"$set": {"meta.is_deleted": True}})
        except Exception as e:
            print('Exception while deleting records in  MongoDB', e)
            logger.debug('Exception while deleting records in MongoDB as exception: {}'.format(e))

    @reconnect
    def aggregate(self, collection_name, query_list):
        """
        For example:
        db.rooms.aggregate([
           {
              $project: {
                 tasks: {
                    $filter: {
                       input: "$tasks",
                       as: "task",
                       cond: { $and: [{$eq: ["$$task.meta.is_archived", false]}, {$eq: ["$$task.meta.is_deleted", false]}] }
                    }
                 }
              }
           }
        ])

        :param collection_name:
        :param query_list:
        :return:
        """
        try:
            cursor = self.mongo_db[collection_name].aggregate(query_list)
            return list(cursor)
        except Exception as e:
            print('Exception while aggregating  MongoDB', e)
            logger.debug('Exception while aggregating in MongoDB')
