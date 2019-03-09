import requests
import json

add_url = "http://127.0.0.1:5001/addTweet"
check_url = "http://127.0.0.1:5001/checkExists/"

def check_exist(tweet_id):
        response = requests.get(check_url + tweet_id)
        return json.loads(response.text)

def persist_tweet(tweet):
    origial_tweet = tweet
    if "retweeted_status" in tweet: # capture the original tweet informtion instead of retweeter
        origial_tweet = tweet["retweeted_status"]

    data = {}
    media = origial_tweet["entities"]["media"][0]

    data["id"] =  media["id"]
    data["url"] = media["expanded_url"]
    data["date"] = origial_tweet["created_at"]
    data["user_id"] = origial_tweet["user"]["id"]
    data["name"] = origial_tweet["user"]["screen_name"]
    data["count"] = origial_tweet["user"]["followers_count"]

    print(data)
    requests.post(url = add_url, data = data)

