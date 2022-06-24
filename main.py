from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
from twitter_reader import TwitterReader, screen_clear
from os import environ
from tqdm import tqdm
import time
import json

MAX_RESULTS = 10
BATCH = 500
ROUNDS = 2
WAITING_TIME = 10

if __name__ == '__main__':
    screen_clear()
    load_dotenv()
    twitter_key = environ.get('twitter_key')
    twitter_secret = environ.get('twitter_secret')
    twitter_access_token = environ.get('twitter_access_token')
    twitter_access_token_secret = environ.get('twitter_access_token_secret')
    twitter_client = environ.get('twitter_client')
    twitter_woeid_mexico_city = environ.get('twitter_woeid_mexico_city')
    
    twitter_reader = TwitterReader(twitter_key, twitter_secret, twitter_access_token, twitter_access_token_secret, twitter_client)
    
    trending_topics = twitter_reader.get_trending_topics(twitter_woeid_mexico_city)
    query = twitter_reader.defineQuery(trending_topics)
    
    tweets = twitter_reader.capture_streaming(query)
     
    with open('json_data.json', "w", encoding = 'utf-8') as outfile:
        json.dump(tweets, outfile)