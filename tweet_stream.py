import tweepy
import json
import pickle
import logging
from tele_ch_send import send_mess, send_review
from rest_db import check_exist, persist_tweet
from tokens import *

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='bot.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        self.process_json(json.dumps(status._json, indent=2))
        # logger.info(str(status.text).encode("utf-8"))

    def process_json(self, json_string):
        json_tw = json.loads(json_string)
        follower_count = json_tw["user"]["followers_count"]
        if "extended_entities" in json_tw:
            for media in json_tw["extended_entities"]["media"]:
                tweet_id = media["id_str"]
                if check_exist(tweet_id):
                    logger.info("duplicate tweet")
                else:
                    url = media["expanded_url"]
                    if follower_count > 300 : # check if user who shared tweeet is "decent"
                        logger.info("sent %s > %s" % (url, send_mess(url)))
                        persist_tweet(json_tw)
                        
                    else:
                        logger.info("to review %s > %s" % (url, send_review(url)))

                break; #only need first entry if getting tweet link

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode= 'extended')
myStream.filter(track=TRACKERS)