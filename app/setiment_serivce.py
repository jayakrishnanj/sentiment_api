import json
from flask import request, Blueprint
from transformers import pipeline

sentiment_api = Blueprint('sentiment_api', __name__)

nlp = pipeline(task='sentiment-analysis',
               model='nlptown/bert-base-multilingual-uncased-sentiment')

@sentiment_api.route('/sentiment-request', methods=['GET', 'POST'])
def data():
    batch_size = request.args.get('batch_size')
    try:
        jsonObject = json.loads(request.form['data'])
        result = {}
        for file_key, file_data in jsonObject.items():
            result[file_key] = {}
            for key, value in file_data.items():
                i = 0
                result[file_key][key] = {'sentiments':[]}
                for v in value:
                    result[file_key][key]['sentiments'].insert(i, analyze_sentiment(v))
                    i = i + 1
    except Exception as e:
        result = str(e)
    return json.dumps(result)

# Sentiment analysis method.
def analyze_sentiment(text):

    """Get and process result"""

    result = nlp(text)

    sent = ''
    if (result[0]['label'] == '1 star'):
        sent = 'Sev1'
    elif (result[0]['label'] == '2 star'):
        sent = 'Sev2'
    elif (result[0]['label'] == '3 stars'):
        sent = 'Sev3'
    elif (result[0]['label'] == '4 stars'):
        sent = 'Sev4'
    else:
        sent = 'Sev5'

    prob = result[0]['score']

    # Format and return results
    return {'sentiment': sent, 'probability': prob}
