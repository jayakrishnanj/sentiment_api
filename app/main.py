from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from setiment_serivce import sentiment_api
from ticketing_service import ticketing_api
from notification_service import notification_api
import os
import config
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.register_blueprint(sentiment_api)
app.register_blueprint(ticketing_api)
app.register_blueprint(notification_api)

@app.get('/')
def get_root():
    return '<h1>This is the sentiment analysis app</h1>'

@app.route('/sentiment-application')
def index_file():
    try:
     files = os.listdir(config.UPLOAD_PATH)
    except:
     files = [] 
    return render_template('index.html', files=files, step=1)
	
@app.route('/uploader', methods = ['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        uploaded_file.save(os.path.join(config.UPLOAD_PATH, filename))
    return redirect(url_for('index_file'))

@app.route('/get-sentiment-analysis', methods = ['POST'])
def analyse_result():
    if request.form['sentiment']:
        try:
            files = os.listdir(config.UPLOAD_PATH)
        except:
            files = [] 
        result = requests.get(request.host_url + 'get-analysed-data')
        result = json.loads(result.content)
        payload = {
            'data': json.dumps(result['result']),
        }
        response = requests.post(request.host_url + 'sentiment-request', data = payload)
        if response.status_code == 200 and response.content:
            payload = {
                'data': response.content,
                'file_data': json.dumps(result['data']),
                'api': result['api']
            }
            api_config = config.API_CONFIG[result['api']]
            values = format_result(payload)
            notification_response = requests.post(request.host_url + 'send-notification', data = payload)
    return render_template('index.html', values = values, sentiments=json.loads(response.content), notification = 1, step=2, files = files, api_config=api_config)

def format_result(payload):
    jsonObject = json.loads(payload['data'])
    file_info = json.loads(payload['file_data'])
    api = payload['api']
    api_config = config.API_CONFIG[api]
    result = {}
    for file_key, values in jsonObject.items():
        for ticket_id, value in values.items():
            result[ticket_id] = {}
            file_data = file_info[file_key][ticket_id]
            result[ticket_id]['description'] = file_data[api_config['description']]
            result[ticket_id]['title'] = file_data[api_config['title']]
            if 'email' in api_config:
                if 'notification_key' in api_config:
                    result[ticket_id]['email'] = file_data[api_config['email']][api_config['notification_key']]
                else:
                    result[ticket_id]['email'] = file_data[api_config['email']]
            result[ticket_id]['created_date'] = file_data[api_config['created_date']]
            comments = file_data[api_config['comments']]
            if comments:
                last_comment = comments[-1]
                if api_config['comment_body']:   
                    result[ticket_id]['comment'] = last_comment[api_config['comment_body']]
                else:
                    result[ticket_id]['comment'] = last_comment
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
