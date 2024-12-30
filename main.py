from email_funcs import *
from fetch import *
import schedule
import time
from statics import *

def main():
    ensure_config_file()

    new_query = input("Would you like to start a new scheduled delivery? Y/n\n-->")
    if new_query == "y" or new_query == "Y":
        reset_config_file()
    else:
        define_search()
        set_destination()   

    with open('config.json') as config_file:
        config = json.load(config_file)
        API_KEY = config['API_KEY']
        email_password = config['email_password']
        from_address = config['from_address']
        to_address = config['to_address']
        cats = config['catagories']
        topic = config['topic']

    categories = cats
    search = topic
    news_stories = fetch_news(API_KEY, categories, search, limit=3)

    email_body = generate_email_body(news_stories)
    send_email(from_address, to_address, 'Your Top News Stories', email_body, "smtp.gmail.com", 587, email_password)

def reset_config_file():    
    static_keys = ["API_KEY", "email_password", "from_address"]

    default_config = {
            "to_address": "",
            "schedule": "",
            "catagories": "",
            "topic": ""
        }

    if not os.path.exists(config_path):
        print(f"No config file found. Creating default config.json at {config_path}")

        new_config = {
            **default_config,
            "API_KEY": "",
            "email_password": "",
            "from_address": ""
        }
        
    else:
        with open(config_path, "r") as config_file:
            existing_config = json.load(config_file)

        saved_config = {key:existing_config.get(key, "") for key in static_keys}
        new_config = {**default_config, **saved_config}
        print("Search parameters reset to default.")

    with open(config_path, "w") as config_file:
        json.dump(new_config, config_file, indent=4)

def ensure_config_file():
    
    if not os.path.exists(config_path):
        print("No config file found, creating config.json.")

        default_config = {
            "to_address": "",
            "schedule": "",
            "catagories": "",
            "topic": "",
            "API_KEY": "",
            "email_password": "",
            "from_address": ""
        }

        with open(config_path, "w") as config_file:
            json.dump(default_config, config_file, indent=4)

    else:
        print("Config file verified.")

if __name__ == "__main__":
    main()