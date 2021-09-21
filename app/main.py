from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from setiment_serivce import sentiment_api
from ticketing_service import ticketing_api
from notification_service import notification_api
import os
import config
import requests
import json

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
    return render_template('index.html', files=files)
	
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
            notification_response = requests.post(request.host_url + 'send-notification', data = payload)
    return render_template('index.html', sentiments=json.loads(response.content), notification = 1)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
