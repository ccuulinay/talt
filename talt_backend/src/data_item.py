from utils import mongo_helper as mongo
from utils import tools
from config import logger, MONGO_COLLECTION
from bson.objectid import ObjectId
from datetime import datetime
import time


def get_item_by_id(post_id, remove_id=True):
    try:
        item = mongo.getbyID(ObjectId(post_id))
    except Exception as e:
        logger.error(e)
        item = mongo.getbyID(post_id)
    if item:
        if remove_id:
            item.pop("_id")
    return item


def get_item_by_itemid(item_id, remove_id=True):
    try:
        query_body = {"item_id": str(item_id)}
        item = mongo.find_one(query_body, MONGO_COLLECTION)
    except Exception as e:
        logger.error(e)
        raise e
    if item:
        if remove_id:
            item.pop("_id")
    return item


def get_one_raw_item(remove_id=True):
    try:
        query_body = {"status": "raw"}
        item = mongo.find_one(query_body, MONGO_COLLECTION)
        mongo.updateFields(item['_id'], {"status": "reviewing"})
    except Exception as e:
        logger.error(e)
        raise e
    if item:
        if remove_id:
            item.pop("_id")
    return item


def save_item(item):
    '''
    Now it handle upsert by self implemented logic. Should use pymongo upsert to do that.
    :param item:
    :return:
    '''
    logger.debug(item)
    item_id = item["item_id"]
    logger.info(item_id)
    existing_item = get_item_by_itemid(item_id, remove_id=False)
    logger.info(existing_item)
    if existing_item:
        tools.update_dictionary_value(item, existing_item)
        existing_item['update_time'] = datetime.utcnow()# .strftime("%Y%m%d%H%M%S")
        to_save_item = existing_item
        mongo_processor = mongo.update
        # mongo.update(user)
    else:
        item['update_time'] = datetime.utcnow()# .strftime("%Y%m%d%H%M%S")
        to_save_item = item
        mongo_processor = mongo.insert
        # mongo.insert(user)

    mongo_processor(to_save_item)
