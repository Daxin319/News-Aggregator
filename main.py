from fetch import *
from email_funcs import *

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)
        API_KEY = config['API_KEY']
        email_password = config['email_password']

    s_input = input("What are you searching for? Press <Enter> to submit --> ")
    print("What catagories are you interested in?")
    print("General    Science    Sports    Business    Health\nEntertainment    Tech    Politics    Food    Travel")
    cat_input = input("Type your choices separated by a comma and space, then press <Enter> to submit\n--> ")

    categories = "business,tech,entertainment"
    search = s_input
    news_stories = fetch_news(API_KEY, categories, search, limit=3)

    email_body = generate_email_body(news_stories)
    send_email('mailtesterdaemon@gmail.com', 'lylehigg@gmail.com', 'Your Top News Stories', email_body, "smtp.gmail.com", 587, email_password)

if __name__ == "__main__":
    main()