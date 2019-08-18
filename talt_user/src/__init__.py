import os
from flask import Flask
from flask_restplus import Api
from pymongo import MongoClient
from flask_mail import Mail

#Create Flask App Object
application = Flask(__name__)
# Load configuration from config object which defaults to Development
application.config.from_object(os.getenv('FLASK_ENVIRONMENT', 'config.Development'))

# Create mail Object
mail = Mail(application)

# Create MongoDB connection object using Mongo URI and instantiate DB (todo_inventory)
mongo_conn = MongoClient(application.config['MONGO_URI'])
mongo_db = mongo_conn[application.config['DB_NAME']]
logger = application.config['LOGGER']

# Create api object for flask restplus
api = Api(application, title='TALT user',
          description='User auth and todo for TALT.', version=1.0)

