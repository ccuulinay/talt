from flask_restplus import fields
from src import api
from src.utils.date_utils import get_current_time
from flask_restplus import fields, reqparse

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', location='headers')

meta = api.model('meta', {
    'is_deleted': fields.Boolean(default=False)
    , 'created_on': fields.DateTime(default=get_current_time())
    , 'updated_on': fields.DateTime(default=get_current_time())
    , 'created_by': fields.String(default='user')
    , 'updated_by': fields.String(default='user')
})
