from flask import Flask, render_template, request
from setiment_serivce import sentiment_api
from ticketing_service import ticketing_api
from notification_service import notification_api
from cache.FlaskCacheFactory import FlaskCacheFactory
import config
import requests
import json
import plugins.ticketing as ticketing

app = Flask(__name__)

# Register the app with cache factory.
cacheFactory = FlaskCacheFactory(3000)
cacheFactory.register(app)

app.register_blueprint(sentiment_api)
app.register_blueprint(ticketing_api)
app.register_blueprint(notification_api)

@app.get('/')
def get_root():
    return '<h1>This is the sentiment analysis app</h1>'

@app.route('/sentiment-application')
def index_file():
    services = ticketing.get_services()
    return render_template('index.html', services=services, step=1)

@app.route('/get-sentiment-analysis', methods = ['POST'])
def analyse_result():
    if request.form['sentiment']:
        service = request.form['services']
        result = requests.get(request.host_url + 'ticketing-service', params={'name': service})
        result = result.json()
        payload = {
            'data': json.dumps(result['comments']),
        }
        response = requests.post(request.host_url + 'sentiment-service', data = payload)
        if response.status_code == 200 and response.content:
            payload = {
                'sentiments': response.content,
                'service': service,
                'tickets': json.dumps(result['tickets']),
            }
            api_config = config.API_CONFIG[service]
            values = format_result(payload)
            services = ticketing.get_services()
            # notification_response = requests.post(request.host_url + 'send-notification', data = payload)
    return render_template('index.html', values = values, sentiments=json.loads(response.content), notification = 1, step=2, api_config=api_config, services=services)

def format_result(payload):
    jsonObject = json.loads(payload['sentiments'])
    tickets = json.loads(payload['tickets'])
    service = payload['service']
    api_config = config.API_CONFIG[service]
    result = {}
    for values in tickets:
        id = str(values['id'])
        result[id] = {}
        result[id]['description'] = values[api_config['description']]
        result[id]['title'] = values[api_config['title']]
        result[id]['created_date'] = values[api_config['created_date']]
        result[id]['comment'] = jsonObject[id]['value']
        #if 'email' in api_config:
         #   if 'notification_key' in api_config:
                # result[id]['email'] = values[api_config['email']][api_config['notification_key']]
          #  else:
                # result[id]['email'] = values[api_config['email']]
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
