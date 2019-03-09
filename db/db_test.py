import requests

url = "http://127.0.0.1:5001/addTweet"

data={
    'id':2,
    'url':'xyz',
    'date':'20190309',
    'user_id':1351,
    'name':'guy',
    'count':10
}

print(requests.post(url = url, data = data))