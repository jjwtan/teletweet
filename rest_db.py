import requests
import json

add_url = "http://127.0.0.1:5001/addTweet"
check_url = "http://127.0.0.1:5001/checkExists/"

def check_exist(tweet_id):
        response = requests.get(check_url + tweet_id)
        return json.loads(response.text)

def persist_tweet(tweet):
    data = {}
    media = tweet["entities"]["media"][0]

    data["id"] =  media["id"]
    data["url"] = media["expanded_url"]
    data["date"] = tweet["created_at"]
    data["user_id"] = tweet["user"]["id"]
    data["name"] = tweet["user"]["screen_name"]
    data["count"] = tweet["user"]["followers_count"]

    print(data)
    requests.post(url = add_url, data = data)

