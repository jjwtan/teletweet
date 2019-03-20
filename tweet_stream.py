import tweepy
import logging
from tokens import *
from my_stream_listener import MyStreamListener

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='bot.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
try:
    api = tweepy.API(auth)
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended')
    myStream.filter(track=TRACKERS, stall_warnings=True)
except Exception as e:
    logging.error(str(e))