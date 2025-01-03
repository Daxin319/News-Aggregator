# News-Aggregator

A simple program to gather news articles and email them to you once per day.

You need to make sure you have python3 installed, along with the schedule library. You can install it by running the following commands in your console.
```
sudo apt install python3

pip3 install schedule

```

Depending on your system, you may need to use a different package manager.

YOU MUST USE YOUR OWN API KEY AND EMAIL ADDRESS!

I built this program using the free API keys available from https://thenewsapi.com you will need to get your own key to use in the config.json file. Since the git repository does not include this file, you can simply run the program once and it will create the file for you in the same directory as the main.py file and provide prompts to enter your information. If you need to edit these values later you can either edit the config.json file directly or you can delete it and this program will create a new file on the next run.
