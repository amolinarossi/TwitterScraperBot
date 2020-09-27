# TwitterScraperBot
The purpose of this project is to imitate the Twitter API with browser automation using Selenium Webdriver.

The following functionalities are currently available:
  login
  basic searching
  advanced searching
  scraping tweets
  
Setup:

Microsoft Edge Browser at https://www.microsoft.com/edge

MSEdge Webdriver at https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads
  must be the same version as your MSEdge browser.
  place this download in the same folder as the TwitterScraperBot.py file

Installing dependencies in your environment:
  pip install msedge-selenium-tools selenium==3.141

Create login.py file and type:
  username = 'your user'
  password = 'your password'

You can run the file in an interactive window or import to your own .py or call the function within the same TwitterScraperBot.py
Example:
  bot = TwitterBot()
  bot.login()
  bot.advancedSearch('rbg', None, None, None, None, None)
  allLines = bot.scrapeTweets(10)
  print('Finished. Check your file for tweets.')

Methods:
  __init__()
    Opens browser.
    Gets https://twitter.com
  goToTwitter()
    Invoke to go to twitter.
  login()
    Invoke to login to twitter.
  basicSearch(topic)
    Argument must be a string.
    Cannot be None.
  advancedSearch(exact, any, none, hashtags, dateFrom, dateTo)
    Arguments must be strings.
    At least one argument must not be None.
  scrapeTweets(desiredNum)
    desiredNum must not be None.
    Saves tweets.csv with desiredNum rows as "data points".
  
