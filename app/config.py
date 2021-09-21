import os
from dotenv import load_dotenv
load_dotenv()

API_CONFIG = {
  "zendesk": {
    "ticket_id": "id",
    "detector": "url",
    "comments": "comments",
    "description": "description",
    "status": "status",
    "comment_body": "plain_body",
    "filters": {
        "status": ["open", "pending"]
      },
     "notification_users": {
        "to": ["assignee"],
        "cc": ["collaborator"]
      },
    "notification_key" : "email",
    #"tag_key": "tags"
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
  "Sev4": "amruta.padale@acquia.com"
}

UPLOAD_PATH = 'uploads'
MAIL_USERNAME = os.getenv('EMAIL')
MAIL_APP_PASS = os.getenv('KEY')
DEVELOPMENT_MODE = True