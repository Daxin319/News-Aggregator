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
    
def check_valid_cats(list):
    valid_cats = ["general", "science", "sports", "business", "health", "entertainment", "tech", "politics", "food", "travel"]
    
    for item in list:
        if item not in valid_cats:
            print("<-------------------------------------Invalid catagories, please try again------------------------------------->")
            return False
        pass
    return True
            