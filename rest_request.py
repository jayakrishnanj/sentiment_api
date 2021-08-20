import requests

query = {'text':'Acquia Search is not working nicely!'}
response = requests.get('http://127.0.0.1:8000/sentiment_analysis/', params=query)
print(response.json())
