import json
from flask import Blueprint
import os
import config
import glob

ticketing_api = Blueprint('ticketing_api', __name__)

@ticketing_api.route('/get-analysed-data', methods = ['GET'])
def process_json():
    list_of_files = glob.glob(config.UPLOAD_PATH + '/*') # * means all if need specific format then *.csv
    file = max(list_of_files, key=os.path.getctime)
    result = {'result': {}, 'data': {}}
    data = load_json_file_data(file)
    api = get_api_to_process(data)
    if api:
        api_config = config.API_CONFIG[api]
        result['result'][file] = {}
        result['data'][file] = {}
        result['api'] = api
        for value in data:
            if validate_api_filter(api, value):
                result['result'][file][value[api_config['ticket_id']]] = []
                comments = value[api_config['comments']]
                result['data'][file][value[api_config['ticket_id']]] = value
                if comments:
                    last_comment = comments[-1]
                    if api_config['comment_body']:     
                        result['result'][file][value[api_config['ticket_id']]].append(last_comment[api_config['comment_body']])
                    else:
                        result['result'][file][value[api_config['ticket_id']]].append(last_comment)
    return json.dumps(result)

# Helper function to check the api details.
def get_api_to_process(values):
    api_to_use = ''
    if values:
        data = values[0]

    if data:
        for key, value in config.API_CONFIG.items():
            if value['detector'] in data and key in data[value['detector']]:
                api_to_use = key
                break

    return api_to_use

# Helper function to validate the filters.
def validate_api_filter(api, data):
    invalid = {}
    api_config = config.API_CONFIG[api]
    if 'filters' not in api_config:
        return True
    for key, value in api_config['filters'].items():
        if key in data:
            if (isinstance (value, list) and data[key] not in value) and (data[key] != value):
                invalid[key] = False

    if not invalid:
        return True
    return False

# Load json files.
def load_json_file_data(file_name):
    data = {}
    if file_name:
        f = open(file_name,)    
        data = json.load(f)
        f.close()
    return data
