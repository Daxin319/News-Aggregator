from fetch import *
from email_funcs import *

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)
        API_KEY = config['API_KEY']
        email_password = config['email_password']

    categories = "business,tech,entertainment"
    search = "Disney"
    news_stories = fetch_news(API_KEY, categories, search, limit=3)

    email_body = generate_email_body(news_stories)
    send_email('mailtesterdaemon@gmail.com', 'lylehigg@gmail.com', 'Your Top News Stories', email_body, "smtp.gmail.com", 587, email_password)

if __name__ == "__main__":
    main()