from dotenv import load_dotenv
from twitter_reader import TwitterReader
import os 


if __name__ == '__main__':
    load_dotenv()
    twitter_key = os.environ.get('twitter_key')
    twitter_secret = os.environ.get('twitter_secret')
    twitter_access_token = os.environ.get('twitter_access_token')
    twitter_access_token_secret = os.environ.get('twitter_access_token_secret')
    twitter_woeid_mexico_city = os.environ.get('twitter_woeid_mexico_city')
    
    twitter_reader = TwitterReader(twitter_key, twitter_secret, twitter_access_token, twitter_access_token_secret)
    
    trending_topics = twitter_reader.get_trending_topics(twitter_woeid_mexico_city)
    
    print("End")
    