from email_funcs import *
from fetch import *
import schedule
import time
from statics import *

def main():
    #verify config file exists, if not create a blank default config.json
    ensure_config_file()

    new_query = input("Would you like to start a new scheduled delivery? Y/n\n-->")
    if new_query == "y" or new_query == "Y":
        # if user requests new search, reset the config file to blank fields and run all functions to refill them with user inputs
        reset_config_file()
        define_search()
        set_destination()
        set_schedule()
    
    # load the config file
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # set schedule functions dependent on user selected intervals
    if config["interval"] == "1":
        # the hours and minutes intervals require a bit of extra code. Lambda function used to start executing the hour/minute interval after the initial start time. Preventing overlapping jobs from occuring.
        schedule.every().day.at(config["start_time"]).do(lambda: (
            fetch_and_send(),
            schedule.every(int(config["interval_number"])).minutes.do(fetch_and_send)
        ))
    if config["interval"] == "2":
        schedule.every().day.at(config["start_time"]).do(lambda: (
            fetch_and_send(),
            schedule.every(int(config["interval_number"])).hours.do(fetch_and_send)
        ))
    if config["interval"] == "3":
        schedule.every(int(config["interval_number"])).days.at(config["start_time"]).do(fetch_and_send)
    if config["interval"] == "4":
        schedule.every(int(config["interval_number"])).weeks.at(config["start_time"]).do(fetch_and_send)

    print("Scheduler is running. Press <Ctrl + C> to stop.")

    # check 1 time per second if there is a scheduled task pending and execute any pending tasks
    while True:
        schedule.run_pending()
        time.sleep(1)


# Reset the config json to blank values for a new search
def reset_config_file():
    # these keys are set by the user in the json file and will not be reset    
    static_keys = ["API_KEY", "email_password", "from_address"]

    # define all mutable configurations as empty fields
    default_config = {
            "to_address": "",
            "start_time": "",
            "interval": "",
            "interval_number": "",
            "catagories": "",
            "topic": ""
        }

    # if no config.json exists, make one
    if not os.path.exists(config_path):
        print(f"No config file found. Creating default config.json at {config_path}")

        key = input("Please enter your API key for your thenewsapi.com account/n-->")
        addy = input("What account will be sending this email?\n-->")
        passw = input("Please enter the password for the sending email account\n-->")

        #set default json config
        new_config = {
            **default_config,
            "API_KEY": key,
            "email_password": passw,
            "from_address": addy
        }
        
    else:
        # if the config file already exists just replace the mutable values and leave the static key value pairs alone
        with open(config_path, "r") as config_file:
            existing_config = json.load(config_file)

        saved_config = {key:existing_config.get(key, "") for key in static_keys}
        new_config = {**default_config, **saved_config}
        print("Search parameters reset to default.")

    #write to file
    with open(config_path, "w") as config_file:
        json.dump(new_config, config_file, indent=4)

def ensure_config_file():
    # check if file exists, if not then create one with all fields present and blank.
    if not os.path.exists(config_path):
        print("No config file found, creating config.json.")

        default_config = {
            "to_address": "",
            "start_time": "",
            "interval": "",
            "interval_number": "",
            "catagories": "",
            "topic": "",
            "API_KEY": "",
            "email_password": "",
            "from_address": ""
        }

        # write default config to file
        with open(config_path, "w") as config_file:
            json.dump(default_config, config_file, indent=4)

    else:
        print("Config file verified.")

# open the config file, pull the news stories from the API, generate the email body, and send the email
def fetch_and_send():
    with open('config.json') as config_file:
        config = json.load(config_file)
        API_KEY = config['API_KEY']
        email_password = config['email_password']
        from_address = config['from_address']
        to_address = config['to_address']
        cats = config['catagories']
        topic = config['topic']

    
    news_stories = fetch_news(API_KEY, cats, topic, limit=3)
    email_body = generate_email_body(news_stories)
    send_email(from_address, to_address, 'Your Top News Stories', email_body, "smtp.gmail.com", 587, email_password)

# set the schedule for email delivery
def set_schedule():
    # input from user for time to start the program
    match = False
    while match == False:
        start_time = input("What time would you like your email to be sent? Use HH:MM in 24 hour format (6:00pm is 18:00, 8:15am is 08:15, etc)\n--> ")
        if not re.fullmatch(r"^([01][0-9]):([0-5][0-9])$", start_time):
            print("Invalid time format, please try again ")
        else:
            match = True
    
    # input from user to determine length of interval units
    interval_match = False
    while interval_match == False:
        interval = input("How long of an interval between emails?\n1 - Minutes\n2 - Hours\n3 - Days\n4 - Weeks\n--> ")
        valid_choices = ["1", "2", "3", "4"]
        if interval not in valid_choices:
            print("Invalid option, please try again.")
        else:
            interval_match = True
    
    # input to determine how many units each interval will be
    number = input("How many minutes/hours/days/weeks between emails?\n--> ")
    
    # set the fields in the config file
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    config["start_time"] = start_time
    config["interval_number"] = number
    config["interval"] = interval

    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=4)


if __name__ == "__main__":
    main() 