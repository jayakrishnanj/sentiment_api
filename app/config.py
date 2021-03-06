import os
from dotenv import load_dotenv
load_dotenv()

API_CONFIG = {
  "ZenDesk": {
    "api_endpoint": "https://acquia.zendesk.com/api/v2/",
    "group_id": "360004942734",
    "ticket_id": "id",
    "tiket_url": "https://acquia.zendesk.com/agent/tickets/",
    "created_date": "created_at",
    "email": "submitter",
    "title": "subject",
    "description": "description",
    "status": "status",
    "comment_body": "plain_body",
    "notification_users": {
      "to": ["assignee"],
      "cc": ["collaborator"]
  },
    "notification_key" : "email",
  },
  "jira" : {
    "ticket_id": "id",
    "comments": "comments",
    "comment_body": "plain_body"
  }
}

PRODUCT_MATRIX = {
  "ac_plus": {
    "Sev1": "aa@acquia.com",
    "Sev2": "bb@acquia.com"
  }
}

EMAIL_MATRIX = {
  "Sev1": "milind.kagdelwar@acquia.com",
  "Sev2": "deep.kachhawa@acquia.com",
  "Sev3": "milind.kagdelwar@acquia.com",
}

EMAIL_INDICATION = {
  "Sev1": "Too Hot",
  "Sev2": "Hot",
  "Sev3": "Warm",
}

UPLOAD_PATH = 'uploads'
MAIL_USERNAME = os.getenv('EMAIL')
MAIL_APP_PASS = os.getenv('KEY')
DEVELOPMENT_MODE = True
STATIC_URL = '/static/'
