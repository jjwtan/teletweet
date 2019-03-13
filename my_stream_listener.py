import tweepy
import logging
from queue import Queue
from threading import Thread
from tweet_processor import process_json

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='bot.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, q = Queue(25)):
        super().__init__()
        self.q = q
        for i in range(3):
            t = Thread(target=self.process_tweets)
            t.daemon = True
            t.start()

    def on_status(self, status):
        # put message into queue
        self.q.put(status._json)
        # logger.info(str(status.text).encode("utf-8"))

    def process_tweets(self):
        while True:
            if self.q.qsize() > 24:
                logging.warn("MAX QUEUE REACHED")
            process_json(self.q.get())
            self.q.task_done()

