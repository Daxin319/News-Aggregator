import http.client, urllib.parse
import json

def fetch_news(api_token, categories, search, limit=50):
    conn = http.client.HTTPSConnection('api.thenewsapi.com')
    params = urllib.parse.urlencode({
        'api_token': api_token,
        'search': search,
        'categories': categories,
        'language': 'en',
        'limit': limit
    })
    
    conn.request('GET', f'/v1/news/all?{params}')
    response = conn.getresponse()
    data = response.read()

    try:
        news = json.loads(data.decode('utf-8'))
        return news.get('data', [])
    except json.JSONDecodeError:
        print('Error decoding JSON response')
        return []