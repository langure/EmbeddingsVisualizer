from datetime import date
from matplotlib.font_manager import json_dump
import tweepy
import json
import uuid
import os
import sys
import jsons

class TwitterStreamingClient(tweepy.StreamingClient):
    def __init__(self, bearer, accumulator):
        super().__init__(bearer)
        self.accumulator = accumulator
    
    def on_tweet(self, tweet):
        #print(tweet.id)
        if tweet.lang == "es" and not tweet.text.startswith("RT"):
            self.accumulator.append(tweet)

class TwitterReader:
    def __init__(self, twitter_key:str, twitter_secret:str, twitter_access_token:str, twitter_access_token_secret:str,
                 twitter_client:str):
        self.twitter_key = twitter_key
        self.twitter_secret = twitter_secret
        self.twitter_access_token = twitter_access_token
        self.twitter_access_token_secret = twitter_access_token_secret
        self.twitter_client = twitter_client
        
        if len(self.twitter_key) < 1:
            raise ValueError("Invalid Twitter key")
        if len(self.twitter_secret) < 1:
            raise ValueError("Invalid Twitter Secret")
        if len(self.twitter_access_token) < 1:
            raise ValueError("Invalid Twitter Access Token")
        if len(self.twitter_access_token_secret) < 1:
            raise ValueError("Invalid Twitter Token Secret")
        if len(self.twitter_client) < 1:
            raise ValueError("Invalid Twitter Token Client")        
        
    def __get_api_handler(self):
        authentication_handler = tweepy.OAuthHandler(self.twitter_key, self.twitter_secret)
        authentication_handler.set_access_token(self.twitter_access_token, self.twitter_access_token_secret)
        return tweepy.API(authentication_handler)
    
    def get_trending_topics(self, woeid:int):
        api_handler = self.__get_api_handler()
        trending_topics_json = api_handler.get_place_trends(woeid)
        trending_topics = json.loads(json.dumps(trending_topics_json, indent=1))
        return trending_topics[0]['trends']
    
    def defineQuery(self, trends) -> str:
        query = ""
        for t in trends:
            if len(query) < 450:
                query = query + t["name"] + " OR "
        return query[:-4]
    
    def capture_streaming(self, query):
        print("Capturing Stream")
        
        accumulator = []
        t = TwitterStreamingClient(self.twitter_client, accumulator)

        old_rule_ids = []
        old_rules = t.get_rules()
        for rule in old_rules.data:
            old_rule_ids.append(rule.id)
        t.delete_rules(old_rule_ids)

        t = TwitterStreamingClient(self.twitter_client, accumulator)
        t.add_rules(tweepy.StreamRule(f"({query})"))
        t.add_rules(tweepy.StreamRule(f"lang:es -is:retweet"))
        
        rules = t.get_rules()
        
        t.filter(expansions = "author_id", 
                 tweet_fields="author_id,entities,geo,source,lang,reply_settings,created_at,public_metrics",
                 threaded=True)
        elements = 0
        
        while elements < 10:
            elements = len(t.accumulator)
        
        t.disconnect()
        
        return jsons.dump(t.accumulator, indent = 4)

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')