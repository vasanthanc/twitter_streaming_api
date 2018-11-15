from tweet_handler import TweetHandler
from tweet_processor import TweetProcessor
import sched, time
from argument_parser import ArgumentParser

'''
this is the root class, which holds all the
functionaliy and giving the rules.
'''


class TweetBase ():

    def __init__(self, query):
        self.tweet_handler = TweetHandler ()
        self.scheduler = sched.scheduler (time.time, time.sleep)
        self.tweet_processor = TweetProcessor ()
        self.query = query

    '''
    this program triggers the start streaming function
    and calling the generate report method,
    This the base most method here.
    '''

    def listen_tweet_and_generate_reports(self):
        try:
            self.tweet_handler.start_stremaing (self.query)
            self.generate_reports ()
        except Exception as e:
            print ('there was some exception occured,', str (e))
        except (KeyboardInterrupt, InterruptedError) as ki:
            print ('quitting')
        finally:
            self.tweet_handler.stop_streaming ()

    '''
    this method is the root method to generate repors from
    the collection of data. this method will execute
    periodically.
    '''

    def generate_reports(self):
        try:
            print ('\n')
            if len (self.tweet_handler.twitter_data_store) == 0:
                pass
                # print ('Zero')
            else:
                self.tweet_processor.tweet_data = self.tweet_handler.twitter_data_store
                self.tweet_processor.print_uniq_user_count ()
                self.tweet_processor.print_domain_related_result ()
                self.tweet_processor.print_unique_words ()
        finally:
            self.scheduler.enter (60, 1, self.generate_reports)
        self.scheduler.run ()


if __name__ == '__main__':
    argument_parser = ArgumentParser ()
    args = argument_parser.parse_args ()
    query = args.query
    tweet__base = TweetBase (query)
    tweet__base.listen_tweet_and_generate_reports ()
