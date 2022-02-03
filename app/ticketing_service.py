from functools import cache
from flask import Blueprint, request
import plugins.ticketing as ticketing
import logging
logger = logging.getLogger('ticketingService')
ticketing_api = Blueprint('ticketing_api', __name__)
from cache.FlaskCacheFactory import cache

@ticketing_api.route('/ticketing-service', methods = ['GET'])
@cache.cached(key_prefix='all_comments')
def get_comments():
    try:
        services = ticketing.get_services()
        service = request.args.get('name')
        if (not service) or (not service in services.values()):
            raise Exception("No service exists with: '" + service + "' name, Please verify the name once.")

        # Load the plugins.
        ticketing.load_plugins('plugins.ticketing.' + service)
        service_class = getattr(ticketing, service)
        service_class = getattr(service_class, service)
        service_object = service_class()
        result = service_object.getData()
    except Exception as e:
        logger.error(str(e))
        result = str(e)
    return result
