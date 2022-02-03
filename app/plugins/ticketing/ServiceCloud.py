import os
from dotenv import load_dotenv
load_dotenv()
import config
import requests
from requests.auth import HTTPBasicAuth

# Credentials for service cloud.
CONFIG = config.API_CONFIG["service_cloud"]

class ServiceCloud:
    
    def __init__(self):
        pass

    # Common funtion to get data.
    def getData(self):
        return []
