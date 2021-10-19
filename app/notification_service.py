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
            email_values['severity'] = value['sentiments'][0]['sentiment']
            email_values['label'] = value['sentiments'][0]['label']
            email_values['url'] = api_config['tiket_url'] + ticket_id
            subject = file_data[api_config['title']]
            if email_values['severity'] in email_mapping:
                to.append(email_mapping[email_values['severity']])
                subject = '[Sentiment App notification] - ' + subject + ' - (' + config.EMAIL_INDICATION[email_values['severity']] + ')'
                response = send_single_email(subject, email_values, to, cc)
    return response

def format_email_values(sentiments, api_config, file_info):
    result = {}
    for file_key, values in sentiments.items():
        for ticket_id, value in values.items():
            result[ticket_id] = {}
            file_data = file_info[file_key][ticket_id]
            result[ticket_id]['title'] = file_data[api_config['title']]
            if 'email' in api_config:
                if 'notification_key' in api_config:
                    result[ticket_id]['email'] = file_data[api_config['email']][api_config['notification_key']]
                else:
                    result[ticket_id]['email'] = file_data[api_config['email']]
            result[ticket_id]['created_date'] = file_data[api_config['created_date']]
    return result

# Send bulk Email utility.
def send_bulk_email(sentiments, api_config, file_info):
    status = True
    to = []
    cc = []
    subject = 'Sentiment App notification - Collaborated'
    email_mapping = config.EMAIL_MATRIX
    # TODO: Remove this line
    to = [email_mapping['Sev1']]
    values = format_email_values(sentiments, api_config, file_info)
    body = render_template('bulk-email.html', sentiments = sentiments, api_config = api_config, values = values)
    send_email(subject, body, to, cc)
    return status

# Send Single Email utility.
def send_single_email(subject, values, to, cc):
    status = True
    body = render_template('email.html', data=values)
    send_email(subject, body, to, cc)
    return status

# Send Email utility.
def send_email(subject, body, to, cc):
    status = True
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = config.MAIL_USERNAME 
        msg['To'] = ", ".join(to)
        if not cc:
            msg['cc'] = ", ".join(cc)
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
