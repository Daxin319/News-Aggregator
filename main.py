from fetch import *
from email_funcs import *

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)
        API_KEY = config['API_KEY']
        email_password = config['email_password']
        from_address = config['from_address']

    s_input = input("What are you searching for? Press <Enter> to submit --> ")
    while True:
        print("What catagories are you interested in?\n")
        print("General    Science    Sports    Business    Health\nEntertainment    Tech    Politics    Food    Travel\n")
        cat_input = input("Type your choices separated by a comma(,), then press <Enter> to submit. You may choose up to 3 catagories.\n--> ")
        cat_input_lower = cat_input.lower()
        cats_list = cat_input.replace(" ", "").split(",")
        print(cats_list)
        num_cats = len(cats_list)
        if check_valid_cats(cats_list) == True:
            break
    
    while True:
        to_input = input("Where would you like your email sent?\n--> ")
        if validate_email(to_input) == True:
            break
        
    categories = cat_input_lower
    search = s_input
    news_stories = fetch_news(API_KEY, categories, search, limit=3)

    email_body = generate_email_body(news_stories)
    send_email(from_address, to_input, 'Your Top News Stories', email_body, "smtp.gmail.com", 587, email_password)

if __name__ == "__main__":
    main()