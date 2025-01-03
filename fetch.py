import http.client, urllib.parse
import json
from datetime import date, timedelta
from email_funcs import *
from statics import *

# function to make the api pull based on user set inputs
def fetch_news(api_token, categories, search, limit=50):
    # set the connection and prepare parameters, this is set to only pull news stories from the last 48 hours.
    conn = http.client.HTTPSConnection('api.thenewsapi.com')
    params = urllib.parse.urlencode({
        'api_token': api_token,
        'search': search,
        'categories': categories,
        'language': 'en',
        'published_after': (date.today()-timedelta(2)).isoformat(),
        'limit': limit
    })
    
    # make the request
    conn.request('GET', f'/v1/news/all?{params}')
    response = conn.getresponse()
    data = response.read()
    
    # decode the response
    try:
        news = json.loads(data.decode('utf-8'))
        return news.get('data', [])
    except json.JSONDecodeError:
        print('Error decoding JSON response')
        return []

# function to check for valid catagories    
def check_valid_cats(list):
    valid_cats = ["general", "science", "sports", "business", "health", "entertainment", "tech", "politics", "food", "travel"]
    
    for item in list:
        if item not in valid_cats:
            print("<-------------------------------------Invalid catagories, please try again------------------------------------->")
            return False
        pass
    return True

# funciton to set all the search fields in the config.json            
def define_search():
    s_input = input("What are you searching for? Press <Enter> to submit --> ")
    while True:
        print("What catagories are you interested in?\n")
        print("General    Science    Sports    Business    Health\nEntertainment    Tech    Politics    Food    Travel\n")
        cat_input = input("Type your choices separated by a comma(,), then press <Enter> to submit. You may choose up to 3 catagories.\n--> ")
        cats_list = cat_input.lower().replace(" ", "").split(",")
        num_cats = len(cats_list)
        if num_cats > 3:
            print("Too many catagories selected, please select a maximum of 3 catagories.")
            continue
        if check_valid_cats(cats_list) == True:
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            
            config["catagories"] = ", ".join(cats_list)
            config["topic"] = s_input
            
            with open(config_path, "w") as config_file:
                json.dump(config, config_file, indent=4)
            
            break

# function to set the destination email address        
def set_destination():
    while True:
        to_input = input("Where would you like your email sent?\n--> ")
        if validate_email(to_input) == True:
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            
            config["to_address"] = to_input
            
            with open(config_path, "w") as config_file:
                json.dump(config, config_file, indent=4)

            break