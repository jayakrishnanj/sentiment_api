import os
from dotenv import load_dotenv
load_dotenv()
import config
import requests
from requests.auth import HTTPBasicAuth

# Credentials for zendesk.
USERNAME = os.getenv('ZENDESK_USER')
PASSWORD = os.getenv('ZENDESK_PASS')
CONFIG = config.API_CONFIG["ZenDesk"]

class ZenDesk:

    def __init__(self):
        pass

    # Common funtion to get data.
    def getData(self):
        result = {
            'tickets': [],
            'comments': [],
        }
        tickets = getTicketData()
        if not tickets:
            return result
        comments = getTicketComment(tickets)
        print(len(result['comments']))
        result['tickets'] = tickets
        result['comments'] = comments
        return result

# Get ticket data.
def getTicketData():
    url = 'search?query=type:ticket group_id:' + CONFIG['group_id'] + '&sort_by=updated_at'
    try:
        response = getApiRequest(url)
        result = response.json()
        return result['results']
    except Exception as e:
        result = str(e)
    return result

# Get ticket comment using id.
def getTicketComment(tickets):
    ticket_comments = {}
    try:
        query = { 'sort_order' : 'desc'}
        for value in tickets:
            response = getApiRequest('tickets/' + str(value['id']) + '/comments.json', query)
            result = response.json()
            ticket_comments[value['id']] = result['comments'][0]['plain_body']
    except Exception as e:
        result = str(e)
    return ticket_comments

# Create API request for zendesk.
def getApiRequest(type, params = {}):
    return requests.get(CONFIG['api_endpoint'] + type, auth=HTTPBasicAuth(USERNAME, PASSWORD), params=params)
