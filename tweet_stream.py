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
        extended_tweet = json.loads(json_string)
        follower_count = extended_tweet["user"]["followers_count"]
        user = extended_tweet["user"]["screen_name"]

        original_tweet = extended_tweet
        if "retweeted_status" in extended_tweet: # capture the original tweet informtion instead of retweeter
            original_tweet = extended_tweet["retweeted_status"]
        try:
            if ("extended_entities" in original_tweet and
                "media" in original_tweet["entities"]):
                
                media = original_tweet["entities"]["media"][0]
                original_follower_count = original_tweet["user"]["followers_count"]
                ori_user = original_tweet["user"]["screen_name"]
                tweet_id = media["id_str"]
                url = media["expanded_url"]

                if check_exist(tweet_id):
                    pass    # alread processed tweet
                else:
                    if follower_count > 600 and original_follower_count > 500:
                        logger.info("sent %s > %s" % (url, send_mess(url)))
                        persist_tweet(original_tweet)
                    else:
                        message = "@%s/@%s\n%s/%s\n%s" % (user, ori_user, follower_count, original_follower_count, url)
                        logger.info("to review %s > %s" % (url, send_review(message)))
        except Exception as e:
            logging.error("oh no %s", str(e))

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode= 'extended')
myStream.filter(track=TRACKERS)