import logging
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from db_controller import DbController
from tweet_util import get_tweet_data, get_user_data, util_screen_tweet

def create_app():
    engine = create_engine("sqlite:///teletweet.db")
  
    # app initiliazation
    app = Flask(__name__)
    db_controller = DbController(engine.connect())

    @app.route('/getTweetsCount', methods=['GET'])
    def get_tweets_count():
        conn = engine.connect()
        count = db_controller.get_tweet_count(conn)
        return jsonify(count)
    
    @app.route('/getAllTweets', methods=['GET'])
    def get_all_tweets():
        conn = engine.connect()
        result = db_controller.get_all_tweets(conn)
        return jsonify({'tweets': [dict(row) for row in result]})

    @app.route('/checkExists/<id>', methods=['GET'])
    def check_id_exists(id):
        conn = engine.connect()
        count = db_controller.get_tweet_of_id(conn, id)
        return jsonify(count >= 1)
    
    @app.route('/screenTweet', methods=['POST'])
    def screen_tweet():
        conn = engine.connect()
        try:
            return jsonify(util_screen_tweet(conn, db_controller, request))
        except Exception as e:
            print("oh no " + str(e))
        return "200"

    @app.route('/addTweet', methods=['POST'])
    def add_tweet():
        conn = engine.connect()
        try:
            tweet_data = get_tweet_data(request)
            user_data = get_user_data(request)
            db_controller.add_tweet(conn, tweet_data, user_data)
        except Exception as e:
            print("oh no " + str(e))
        return "200"



    @app.route('/check', methods=['GET'])
    def health_check():
        return "DB service is working"

    return app


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='db-service.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    app = create_app()
    app.run(port=5001, host='0.0.0.0')  #set host to allow external access