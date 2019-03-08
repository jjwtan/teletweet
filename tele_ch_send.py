import requests
from tokens import *

# telegram url
url = "https://api.telegram.org/bot" + BOT_TOKEN

def send_mess(text):
    params = {'chat_id':CH_BOT, 'text': text}
    response = requests.post(url + "/sendMessage", data=params)
    return response

def send_review(text):
    params = {'chat_id':REV_BOT, 'text': text}
    response = requests.post(url + "/sendMessage", data=params)
    return response
