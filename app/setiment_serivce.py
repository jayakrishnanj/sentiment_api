import json
from flask import request, Blueprint
from transformers import pipeline
from cache.FlaskCacheFactory import cache

sentiment_api = Blueprint('sentiment_api', __name__)

nlp = pipeline(task='sentiment-analysis',
               model='nlptown/bert-base-multilingual-uncased-sentiment')

@sentiment_api.route('/sentiment-service', methods=['POST'])
def get_sentiment():
    batch_size = request.args.get('batch_size')
    try:
        jsonObject = json.loads(request.form['data'])
        result = {}
        for key, value in jsonObject.items():
            # TODO: Change the approach here.
            value = value[:512]
            result[key] = analyze_sentiment(value)
    except Exception as e:
        result = str(e)
    return result

# Sentiment analysis method.
def analyze_sentiment(text):

    """Get and process result"""

    result = nlp(text)

    sent = ''
    label = ''
    if (result[0]['label'] == '1 star'):
        sent = 'Sev1'
        label = 'Very Negative'
    elif (result[0]['label'] == '2 star'):
        sent = 'Sev2'
        label = 'Negative'
    elif (result[0]['label'] == '3 stars'):
        sent = 'Sev3'
        label = 'Neutral'
    elif (result[0]['label'] == '4 stars'):
        sent = 'Sev4'
        label = 'Positive'
    else:
        sent = 'Sev5'
        label = 'Very Positive'

    prob = result[0]['score']

    # Format and return results
    return {'sentiment': sent, 'probability': prob, 'label': label, 'value': text }
