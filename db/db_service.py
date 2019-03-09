from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from db_controller import DbController

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

    @app.route('/checkExists/<id>', methods=['GET'])
    def check_id_exists(id):
        conn = engine.connect()
        count = db_controller.get_tweet_of_id(conn, id)
        return jsonify(count >= 1)

    @app.route('/addTweet', methods=['POST'])
    def add_tweet():
        conn = engine.connect()
        try:
            tweet_data = (
                int(request.values["id"]),
                request.values["url"],
                request.values["date"],
                int(request.values["user_id"])
            )
            user_data = (
                int(request.values["user_id"]),
                request.values["name"],
                int(request.values["count"])
            )
            db_controller.add_tweet(conn, tweet_data, user_data)
        except Exception as e:
            print("oh no " + str(e))
        return "200"



    @app.route('/check', methods=['GET'])
    def health_check():
        return "DB service is working"

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5001)