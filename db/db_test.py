import requests

url = "http://127.0.0.1:5001/addTweet"
screen_url = "http://127.0.0.1:5001/screenTweet"

data={
    'id':2,
    'url':'xyz',
    'date':'20190309',
    'user_id':1351,
    'name':'sxxx',
    'count':10
}

# print(requests.post(url = url, data = data))

# print(requests.get("http://127.0.0.1:5001/getAllTweets"))

print(requests.post(url = screen_url, data = data).content)
