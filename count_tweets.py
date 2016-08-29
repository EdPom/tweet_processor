import time
import memcache
import psycopg2

def count(term, cur, conn, mc):
    # Given the newest tweet, find the number of tweets that are at most
    # 10 minutes older than this tweet.
    cur.execute("SELECT count(tweet.created_at) FROM {}_tweets tweet WHERE tweet.created_at >= (SELECT MAX(created_at) FROM {}_tweets) - interval '10 minutes';".format(term, term))
    ret = cur.fetchone()[0]
    conn.commit()
    # Then store this number in memcache with key '<term>_count'
    mc.set(term + '_count', ret)

# Connect to memcached
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# Connect to redshift
conn = psycopg2.connect(
    host="SQL_SERVER_ADDRESS",
    user='SQL_SERVER_USER',
    port=PORT_NUMBER,
    password='SQL_SERVER_PASSWORD',
    dbname='DB_NAME')
cur = conn.cursor()

while True:
    count('basketball', cur, conn, mc)
    count('baseball', cur, conn, mc)
    time.sleep(30)
