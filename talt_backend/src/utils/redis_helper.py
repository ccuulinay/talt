from config import REDIS_SERVER, REDIS_PASS, REDIS_PORT, logger, REDIS_NODE
import json
import redis
from rediscluster import StrictRedisCluster
import threading
import time


jscode_prefix = "wechat:user:jscode:"
jscode_max_age = 300

LIFETIME = 60 * 5  # 30 mins lifetime
LAST = time.time()
VERSION = 1
if REDIS_NODE != "Single":
    startup_nodes = [{"host": REDIS_SERVER, "port": REDIS_PORT}]
    pool_cluster = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True,
                                      skip_full_coverage_check=True)
    redis_getter = pool_cluster.get
    redis_setter = pool_cluster.set
    redis_expire = pool_cluster.expire
else:
    pool = redis.ConnectionPool(host=REDIS_SERVER, port=REDIS_PORT, db=0, decode_responses=True,)  # , password=REDIS_PASS
    redis_getter = redis.Redis(connection_pool=pool).get
    redis_setter = redis.Redis(connection_pool=pool).set
    redis_expire = redis.Redis(connection_pool=pool).expire

def connect():
    if(time.time() - LAST > 60):
        global redis_getter
        global redis_setter
        global redis_expire
        if REDIS_NODE != "Single":
            startup_nodes = [{"host": REDIS_SERVER, "port": REDIS_PORT}]
            pool_cluster = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True,
                                              skip_full_coverage_check=True)
            redis_getter = pool_cluster.get
            redis_setter = pool_cluster.set
            redis_expire = pool_cluster.expire
        else:
            try:
                pool = redis.ConnectionPool(host=REDIS_SERVER, port=REDIS_PORT, db=0, decode_responses=True,)  # , password=REDIS_PASS
                redis_getter = redis.Redis(connection_pool=pool).get
                redis_setter = redis.Redis(connection_pool=pool).set
                redis_expire = redis.Redis(connection_pool=pool).expire
            except:
                logger.critical("Could not connect to Redis")
        logger.debug("REDIS Re-connected")


def get_jscode_session(jscode):
    wx_user = redis_getter(jscode_prefix+jscode)
    if wx_user:
        return json.loads(wx_user)


def set_jscode_session(jscode, wx_user):
    wx_user['created_time'] = time.time()
    logger.debug(wx_user)
    json_out = json.dumps(wx_user)
    redis_setter(jscode_prefix+jscode, json_out)
    redis_expire(jscode_prefix+jscode, jscode_max_age)

