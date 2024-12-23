from fetch import *
from email_funcs import *

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)
        API_KEY = config['API_KEY']

    categories = "business,tech,entertainment"
    search = "Disney"
    news_stories = fetch_news(API_KEY, categories, search, limit=10)

    email_body = generate_email_body(news_stories)
    print(email_body)

if __name__ == "__main__":
    main()