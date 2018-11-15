from tweepy.streaming import StreamListener
from json import loads

"""
This is a listener class, this class will trigger
events when new tweet posted.
"""


class Twitterlistener (StreamListener):

    def __init__(self, store, api=None):
        StreamListener.__init__ (self, api=api)
        self._stop = False
        self.data_store = store

    def stop_listening(self):
        self._stop = True

    def on_data(self, data):
        if self._stop:
            return False
        else:
            # pass
            # print(data)
            data_object = loads (data)
            if not data_object['text'].startswith ('RT'):
                self.data_store.append (data_object)
        return True

    def on_status(self, status):
        print ('ON STATUS', status)

    def on_error(self, status_code):
        if status_code == 420:
            print ('- Rate limit {} -'.format (status_code))
            return False
        else:
            print (status_code)

    def on_limit(self, track):
        print ("LIMIT: ", track)

    def on_timeout(self):
        print ("TIMEOUT!")