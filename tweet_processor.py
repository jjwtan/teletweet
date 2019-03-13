import json
import logging
from tele_ch_send import send_mess, send_review
from rest_db import check_exist, persist_tweet, screen_tweet
from tokens import *

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='bot.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    
def process_json(json_string):
    extended_tweet = json.loads(json.dumps(json_string))
    follower_count = extended_tweet["user"]["followers_count"]
    user = extended_tweet["user"]["screen_name"]

    original_tweet = extended_tweet
    if "retweeted_status" in extended_tweet: # capture the original tweet informtion instead of retweeter
        original_tweet = extended_tweet["retweeted_status"]
    print(str(original_tweet["text"]).encode('utf-8'))
    try:
        if ("extended_entities" in original_tweet and
            "media" in original_tweet["entities"]):
            
            media = original_tweet["entities"]["media"][0]
            original_follower_count = original_tweet["user"]["followers_count"]
            ori_user = original_tweet["user"]["screen_name"]
            tweet_id = media["id_str"]
            url = media["expanded_url"]

            if check_exist(tweet_id):
                pass    # already processed tweet
            else:
                if follower_count > 600 and original_follower_count > 500 and screen_tweet(original_tweet):
                    logging.info("sent %s > %s" % (url, send_mess(url)))
                    persist_tweet(original_tweet)
                else:
                    message = "@%s/@%s\n%s/%s\n%s" % (user, ori_user, follower_count, original_follower_count, url)
                    logging.info("to review %s > %s" % (url, send_review(message)))
    except Exception as e:
        logging.error("oh no %s", str(e))