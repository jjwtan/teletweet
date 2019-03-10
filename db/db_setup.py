import sqlite3
import sys

def create_table(conn, create_table_sql):
    try:
        conn.execute(create_table_sql)
    except sqlite3.OperationalError as e:
        print ("SQL Execution -", e)

def init_tables(conn):
    create_table(
        conn, 
        '''CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY, 
            expanded_url TEXT,
            created_at TEXT,
            user_id INTEGER
        )'''
    )

    create_table(
        conn, 
        '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            screen_name TEXT,
            follower_count INTEGER
        )'''
    )

    create_table(
        conn, 
        '''CREATE TABLE IF NOT EXISTS blacklist (
            id INTEGER PRIMARY KEY, 
            screen_name TEXT
        )'''
    )

