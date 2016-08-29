from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import logging
from logging.handlers import RotatingFileHandler
import time

# setting up Twitter API credentials
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

# Term to track on Twitter
track_term = 'basketball'

# Location to store the log
log_path = '/tmp/' + track_term + '.log'

# Setting up rotating logger
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_path, maxBytes=2097152, backupCount=2)
logger.addHandler(handler)

class LogListener(StreamListener):
    def on_data(self, data):
        d = json.loads(data)
        # From the tweet record we will only store id_str and created_at
        d_temp = ''
        # Timestamp from Twitter has to be processed before it can be
        # inserted into Redshift / PostgreSQL
        d_temp += time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(d['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
        d_temp += ','
        d_temp += d['id_str']
        logger.info(d_temp)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = LogListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=[track_term])
