import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np
import pandas as pd

import os

### Twitter Client ###
class TwitterClient():
    # This class Builds up a "Client" in a sense that, it creates an API object to which a lot of functionality has been provided by Twitter API through Tweepy
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_api()
        self.twitter_client = tweepy.API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client
    
    
### Twitter Authenticator ###
class TwitterAuthenticator():
    # This class has a method which returns an Auth object to which credentials has been set up. We can use it further to authorise ourselves before using a Twitter API service
    def authenticate_twitter_api(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

### Twitter Streamer ###
class TwitterStreamer():
    # Class For streaming and processing live tweets
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, keywords_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_api()

        stream = Stream(auth, listener)
        
        stream.filter(track=keywords_list)

### Twitter Listener ###
# A class inherited from StreamListener Class, that just listens for the tweets, and decides what to do when data is received or when an error occurs
class TwitterListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    # Instead calling it a tweet, i have called data because tweets will be returned as str. Uff!
    def on_data(self, data):
        try:
            print(data)

            with open(self.fetched_tweets_filename, 'a') as tf:

                if(os.stat(self.fetched_tweets_filename).st_size!=0):
                    tf.write(',')
                elif(os.stat(self.fetched_tweets_filename).st_size==0):
                    tf.write('[\n')

                tf.write(data)
            return True


        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        if status == 420:
            # Returning false on_data method in case rate limit
            return False
        print("Error Status: ", status)

    def on_disconnect(self, notice):
        print("Stream has been Disconnected! Notice: ", notice)
        return False
    

# A class with Methods to Store Tweets in a csv file or to make a Pandas Dataframe
class TweetAnalyzer():
    # Funcionality for analyzing and categorizing content from tweets
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[[tweet.text, tweet.author.screen_name, tweet.user.screen_name, tweet.contributors, tweet.id, tweet.id_str, tweet.source, tweet.source_url, tweet.coordinates, tweet.destroy, tweet.truncated, tweet.entities, tweet.created_at, tweet.favorite, tweet.favorite_count, tweet.favorited, tweet.geo, tweet.retweet, tweet.retweet_count, tweet.retweeted, tweet.retweets, tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id, tweet.in_reply_to_user_id_str, tweet.is_quote_status, tweet.lang, tweet.parse, tweet.parse_list, tweet.place] for tweet in tweets], columns=['Text', 'Author', 'User', 'Contributors', 'Id', 'Id_str', 'Source', 'Source_url','Coordinates', 'Destroy', 'Truncated','Entities', 'Created_at', 'favorite', 'favorite_count', 'favorited', 'geo', 'Retweet', 'Retweet_count', 'Retweeted', 'Retweets', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_user_id_str', 'is_quote_status', 'Language', 'Parse', 'Parse_list', 'Place'] )
        return df
    
    def tweets_to_csv(self, tweets):
        df = self.tweets_to_data_frame(tweets)
        df.to_csv("Twitter-data.csv")
        return df



if __name__ == "__main__":
    twitter_client = TwitterClient()
    twitter_streamer = TwitterStreamer()
    fetched_tweets_filename="Twitter-streamer-data.json"


    ########## PUT YOUR KEYWORDS OVER HERE ##########
    keywords_list = []

    try:
        twitter_streamer.stream_tweets(fetched_tweets_filename=fetched_tweets_filename, keywords_list=keywords_list)

    except KeyboardInterrupt:
        with open(fetched_tweets_filename, 'a') as tf:
            tf.write(']')
    
    
    