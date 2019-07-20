import os
import logging

APP_NAME = 'Tag-And-Label-Tool'

# logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(APP_NAME)


# WX
WX_APP_ID = os.getenv("WX_APP_ID", 'wxd929b5cebc51510d')
WX_APP_SECRET = os.getenv("WX_APP_SECRET", '2975fc525242dd5688193030dd65adb2')
WX_AUTH_API = os.getenv("WX_AUTH_API", 'https://api.weixin.qq.com/sns/jscode2session')

HTTP_PORT = os.getenv('HTTP_PORT', 6074)
CACHE_TIMEOUT = 60 * 60  # 60 minutes


# Mongo
MONGO_SERVER = os.getenv("MONGO_SERVER", "localhost")  # server.dsinn.co
MONGO_PORT = os.getenv("MONGO_PORT", 27017)  # 32769 or 27017
MONGO_DB = 'talt-dev'
MONGO_COLLECTION = 'backend'


# Redis
REDIS_SERVER = os.getenv('REDIS_SERVER', "localhost")  # server.dsinn.co
REDIS_PASS = os.getenv('REDIS_PASS', "0HnWdaZ51JciF68IoDJMTNTDqvhtJ4S8AKZVS3xiAcwnNV0VDyhbESfAYEooDdZG")
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_NODE = os.getenv('REDIS_NODE', "Single") # Possible Value should be "Single" or "Cluster"