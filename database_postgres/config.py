import sys
import psycopg2

con = cur = None

def connect():
    global con, cur
    try:
        con = psycopg2.connect(user="postgres",
                                  password="o48wktKBegNqQ7rI",
                                  host="172.16.18.47",
                                  port="5432",
                                  database="thu_py")
        cur = con.cursor()
    except psycopg2.DatabaseError as e:
        if con:
             con.rollback()
        print(e)
        sys.exit


def get_db():
    if not (con and cur):
        connect()
    return (con, cur)