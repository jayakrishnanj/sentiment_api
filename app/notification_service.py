import json
from flask import config, request, Blueprint, render_template
import config
import smtplib
from email.message import EmailMessage

notification_api = Blueprint('notification_api', __name__)

@notification_api.route('/send-notification', methods=['POST'])
def notify():
    response = False
    email_mapping = config.EMAIL_MATRIX
    jsonObject = json.loads(request.form['data'])
    file_info = json.loads(request.form['file_data'])
    api = request.form['api']
    api_config = config.API_CONFIG[api]
    email_values = {}
    for file_key, values in jsonObject.items():
        for ticket_id, value in values.items():
            file_data = file_info[file_key][ticket_id]
            to =[]
            cc = []
            if config.DEVELOPMENT_MODE != True:
                cc = build_cc(file_data, api_config)
                to = build_to(file_data, api_config)
            email_values['ticket_id'] = ticket_id
            email_values['description'] = file_data[api_config['description']]
            email_values['status'] = file_data[api_config['status']]
            email_values['severity'] = value['sentiments'][0]['label']
            email_values['url'] = api_config['tiket_url'] + ticket_id
            if email_values['severity'] in email_mapping:
                to.append(email_mapping[email_values['severity']])
                subject = '[' + email_values['severity'] + '] : Sentiment App notification'
                response = send_email(subject, email_values, to, cc)
    return response

# Send Email utility.
def send_email(subject, values, to, cc):
    status = True
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = config.MAIL_USERNAME 
        msg['To'] = ", ".join(to)
        if not cc:
            msg['cc'] = ", ".join(cc)
        body = render_template('email.html', data=values)
        msg.set_content(body, subtype='html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(config.MAIL_USERNAME, config.MAIL_APP_PASS) 
            smtp.send_message(msg)
    except Exception as ex:
        status = False
    return status

def build_to(file_data, api_config):
    notification_key = api_config['notification_key']
    to = []
    if 'notification_users' in api_config:
        users = api_config['notification_users']
        if 'to' in users:
            for to_user in users['to']:
                to_data = file_data[to_user]
    if isinstance(to_data, list):
        for data in to_data:
            to.append(data[notification_key])
    else:
        to.append(to_data[notification_key])

    return to

def build_cc(file_data, api_config):
    notification_key = api_config['notification_key']
    cc = []
    if 'notification_users' in api_config:
        users = api_config['notification_users']
        if 'cc' in users:
            for cc_user in users['cc']:
                cc_data = file_data[cc_user]

    if isinstance(cc_data, list):
        for data in cc_data:
            cc.append(data[notification_key])
    else:
        cc.append(cc_data[notification_key])

    return cc
