import tweepy
import json

class TwitterReader:
    def __init__(self, twitter_key:str, twitter_secret:str, twitter_access_token:str, twitter_access_token_secret:str):
        self.twitter_key = twitter_key
        self.twitter_secret = twitter_secret
        self.twitter_access_token = twitter_access_token
        self.twitter_access_token_secret = twitter_access_token_secret
        
        if len(self.twitter_key) < 1:
            raise ValueError("Invalid Twitter key")
        if len(self.twitter_secret) < 1:
            raise ValueError("Invalid Twitter Secret")
        if len(self.twitter_access_token) < 1:
            raise ValueError("Invalid Twitter Access Token")
        if len(self.twitter_access_token_secret) < 1:
            raise ValueError("Invalid Twitter Token Secret")
        
    def __get_api_handler(self):
        authentication_handler = tweepy.OAuthHandler(self.twitter_key, self.twitter_secret)
        authentication_handler.set_access_token(self.twitter_access_token, self.twitter_access_token_secret)
        return tweepy.API(authentication_handler)
    
    def get_trending_topics(self, woeid:int):
        api_handler = self.__get_api_handler()
        trending_topics_json = api_handler.get_place_trends(woeid)
        trending_topics = json.loads(json.dumps(trending_topics_json, indent=1))
        return trending_topics[0]['trends']