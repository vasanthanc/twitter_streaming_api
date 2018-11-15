import settings
from tweepy import Stream
from tweepy import API
from tweepy import OAuthHandler
from twitter_api_listener import Twitterlistener
from threading import Thread

'''
TweetHandler will take care of start, making async listen and
closing the connection.
'''


class TweetHandler ():

    def __init__(self):
        self._auth = OAuthHandler (settings.USER_KEY_VARIABLES['CONSUMER_VARIABLES']['CONSUMER_KEY'],
                                   settings.USER_KEY_VARIABLES['CONSUMER_VARIABLES']['CONSUMER_SECRET'])
        self._auth.set_access_token (settings.USER_KEY_VARIABLES['ACCESS_VARIABLES']['ACCESS_TOKEN'],
                                     settings.USER_KEY_VARIABLES['ACCESS_VARIABLES']['ACCESS_SECRET'])
        self._api = API (self._auth, wait_on_rate_limit=True)
        self.twitter_data_store = []
        self.track_key = None

    '''
    function will create a thread to listen
    new tweets, and the tweets will push to an
    array, which is initialized in constructor.
    '''

    def start_stremaing(self, track_key):
        self.track_key = track_key
        self.twitter_listener = Twitterlistener (self.twitter_data_store, self._api)
        twitter_stream = Stream (self._auth, self.twitter_listener, tweet_mode='extended')
        print ('Start streaming')
        filter = twitter_stream.filter
        self.thread_stream = Thread (target=filter, kwargs={'track': [self.track_key]})
        self.thread_stream.start ()

    '''
    when function triggers, we are closing the connection
    and ending the thread.
    '''

    def stop_streaming(self):
        if not self.twitter_listener:
            print ("No stream to stop.")
            return
        print ("Stopping stream.")
        self.twitter_listener.stop_listening ()
        self.thread_stream.join ()
        self.twitter_listener = None
