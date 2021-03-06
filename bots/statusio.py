# # TwitterBot/bots/statusbot.py

"""
- [x] Add the randomness of the Hashtags bot picks from the pull of hashtags
- [ ] Create a function which tweets about the articles found on Economist
- [ ] Create a function which tweets about the tech world news
- [ ] Create a function which tweets about video games on Sundays
"""

import json
import tweepy
import logging
import requests
import random
import time
import dayandtime as dat

from bs4 import BeautifulSoup
from cfg import create_api


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

class StatusUpdate():
    """Bot Statusio - scraps the web-page for the new articles.

    Determins what day of the week it is, scraps articles
    from the predetermined pages and starts tweeting them.
    """
    
    def __init__(self, api):
        self.api = api
        self.soups = [BeautifulSoup(requests.get(f'https://www.datasciencecentral.com/page/search?q={i}').text,
                        'html.parser') for i in ['AI', 'Machine+Learning', 'Deep+Learning']]

    def ds_central(self):
        ai_hashtags = ['DataScience', 'AI', 'MachineLearning', 'DataAnalytics', 'DataViz', 'BigData',
                    'ArtificialIntelligence', 'data', 'python', 'DeepLearning']
        try:
            for s in self.soups:
                for i in s.find_all('a', href=True, text=True):
                    if i['href'].startswith('https://www.datasciencecentral.com/profiles/blogs'):
                        if i.string.startswith(('Subscribe', 'subscribe', 'See', 'More', 'Old')):
                            pass
                        else:
                            hashtag = ''
                            for h in random.sample(ai_hashtags, k=3): # Pick three unique random hashtags from the list.
                                hashtag += " #" + str(h)             
                            self.api.update_status(str(i.string + ' >> ' + i['href']) + hashtag)
        except:
            self.api.update_status("How's your Data Science project going? #DataScience #MachineLearning #AI")


def main():
    api = create_api()
    # today = dat.find_day(dat.today())
    # while today in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
    while True:
        try:
            LOGGER.info(f'Today is a {today}, time to start posting')
            StatusUpdate(api).ds_central()
        except:
            LOGGER.info('waiting')
            time.sleep(300)
    # else:
        # print('Today is', today, 'I have an off')

if __name__ == '__main__':
    main()
