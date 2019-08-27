from flask_restplus import marshal
from flask_jwt_extended import get_jwt_identity
from src.utils.date_utils import get_current_time


def custom_marshal(model, template, option='create', prefix=""):
    email = get_jwt_identity()
    data = marshal(model, template)
    if option == 'create':
        data['meta']['created_on'] = get_current_time()
        data['meta']['updated_on'] = get_current_time()
        data['meta']['created_by'] = email
        data['meta']['updated_by'] = email
    elif option == 'update' or option == 'delete':
        if prefix:
            mod_data = {}
            for key, value in data.items():
                mod_data[prefix + "." + key] = value
            data[prefix + "." + 'meta.updated_on'] = get_current_time()
            data[prefix + "." + 'meta.updated_by'] = email
            data = mod_data
        else:
            data['meta']['updated_on'] = get_current_time()
            data['meta.updated_by'] = email
    return data


def update_common_payload(prefix=""):
    email = get_jwt_identity()
    data = {}
    if prefix:
        data[prefix + "." + 'meta.updated_on'] = get_current_time()
        data[prefix + "." + 'meta.updated_by'] = email
    else:
        data['meta.updated_on'] = get_current_time()
        data['meta.updated_by'] = email

    return data