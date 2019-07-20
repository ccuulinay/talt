import pymongo
from config import MONGO_SERVER, MONGO_PORT, MONGO_DB, MONGO_COLLECTION
import functools
import time
import logging
from bson.objectid import ObjectId

# connect to server
myclient = pymongo.MongoClient("mongodb://{}:{}/".format(MONGO_SERVER, MONGO_PORT))
mongo = myclient[MONGO_DB]

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
                logging.warning("PyMongo auto-reconnecting... %s. Waiting %.1f seconds.", str(e), wait_t)
                time.sleep(wait_t)

    return wrapper


@reconnect
def insert(item, collection=MONGO_COLLECTION):
    c = mongo[collection]

    if isinstance(item, list):
        c.insert_many(item)
    else:
        c.insert(item)


@reconnect
def updateFields(id, fields, collection=MONGO_COLLECTION):
    c = mongo[collection]
    query = {"$set": fields}
    c.update_one({'_id': id}, query, upsert=True)


@reconnect
def update(item, collection=MONGO_COLLECTION):
    c = mongo[collection]
    c.update({'_id': item['_id']}, item, upsert=True)


@reconnect
def delete(id, collection=MONGO_COLLECTION):
    c = mongo[collection]
    c.delete_one({'_id': id})


@reconnect
def getbyID(id, collection=MONGO_COLLECTION):
    mycol = mongo[collection]
    return mycol.find_one({'_id': id})


@reconnect
def find(query, collection, s=None, skip=0, limit=1e9, projection=None):
    mycol = mongo[collection]
    l = int(limit)
    if s:
        myresults = mycol.find(query, projection).sort(s).skip(skip).limit(l)
    else:
        myresults = mycol.find(query, projection).skip(skip).limit(l)
    results = []
    for r in myresults:
        results.append(r)
    return results


@reconnect
def find_one(query, collection):
    mycol = mongo[collection]
    return mycol.find_one(query)


@reconnect
def search(query, collection):
    mycol = mongo[collection]
    res = mycol.find(query)
    return res
