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
        
    def get_all_tweets(self, conn):
        sql = "SELECT tweets.id, expanded_url, created_at, user_id, screen_name, follower_count FROM tweets JOIN users ON tweets.user_id = users.id ORDER BY tweets.id ASC"
        results = conn.execute(sql)
        return results.fetchall()

    def add_tweet(self, conn, tweet_data, user_data):
        tweet_sql = "INSERT INTO tweets VALUES (?,?,?,?)"
        user_sql = "INSERT INTO users VALUES (?,?,?)"

        conn.execute(tweet_sql, tweet_data)
        conn.execute(user_sql, user_data)

    def get_blacklist(self, conn):
        sql = "SELECT * FROM blacklist"
        results = conn.execute(sql)
        return results.fetchall()

    def add_blacklist_user(self, conn, user):
        sql = "INSERT INTO blacklist VALUES ((SELECT id FROM users WHERE screen_name = '%s'),'%s')" % (user, user)
        conn.execute(sql)

    def delete_blacklist_user(self, conn, user):
        sql = "DELETE FROM blacklist WHERE screen_name = '%s'" % user
        conn.execute(sql)



    

    
