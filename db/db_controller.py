import sqlite3
from db_setup import init_tables

class DbController(object):

    def __init__(self, conn):
        init_tables(conn)

    def get_tweet_count(self, conn):
        query = conn.execute("SELECT count(*)FROM tweets")
        return query.first()[0]

    def get_tweet_of_id(self, conn, id):
        sql = "SELECT count(*) FROM tweets WHERE id=%s" % id
        query = conn.execute(sql)
        return query.first()[0]
        
    
    def add_tweet(self, conn, tweet_data, user_data):
        tweet_sql = "INSERT INTO tweets VALUES (?,?,?,?)"
        user_sql = "INSERT INTO users VALUES (?,?,?)"

        conn.execute(tweet_sql, tweet_data)
        conn.execute(user_sql, user_data)



    

    
