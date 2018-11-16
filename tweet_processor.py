import pandas as panda
from json import load
from urllib.parse import urlsplit
import nltk
import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

'''
text processing algorithms are handled in this class
'''


class TweetProcessor ():
    def __init__(self):
        self._tweet_data = None
        self.data_frame = None

    @property
    def tweet_data(self):
        pass

    @tweet_data.setter
    def tweet_data(self, data):
        self._tweet_data = data

    '''
    getting urls from tweet data and appending to
    array list.
    '''

    def get_url_entities(self):
        self.url_entity_pool = []
        for tweets_data in self._tweet_data:
            if 'extended_tweet' in tweets_data:
                urls = tweets_data['extended_tweet']['entities']['urls']
                if len (urls) == 0:
                    pass
                else:
                    for url in urls:
                        extended_url = url['expanded_url'] if ('expanded_url' in url) else url['url']
                        self.url_entity_pool.append (extended_url)
            else:
                urls = tweets_data['entities']['urls']
                if len (urls) == 0:
                    pass
                else:
                    for url in urls:
                        extended_url = url['expanded_url'] if ('expanded_url' in url) else url['url']
                        self.url_entity_pool.append (extended_url)

    '''
    parsing the url and getting only the domain name
    and push to uniq domain vatiable.
    '''

    def parse_urls_and_get_only_domain(self):
        self.get_url_entities ()
        self.domain_pool = []
        for url in self.url_entity_pool:
            base_url = "{0.scheme}://{0.netloc}/".format (urlsplit (url))
            self.domain_pool.append (base_url)
        domain_dataframe = panda.DataFrame ({'domains': self.domain_pool})
        self.uniq_domain = domain_dataframe.domains.value_counts ().to_dict ()

    '''
    this will print out the url related result.
    '''

    def print_domain_related_result(self):
        self.parse_urls_and_get_only_domain ()
        print ('\n')
        print ('There are, {} urls exist in tweets -'.format (len (self.url_entity_pool)))
        for k, v in self.uniq_domain.items ():
            print ('{: >10} -> {}'.format (k, v))

    '''
    we have large informations in json, here I'm trying to
    filterout only some of the fields among.
    so we can easyly create dataframe.
    '''

    def make_csv_data(self):
        self.csv_data = []
        for tweets_data in self._tweet_data:
            tweet_csv = []
            tweet_csv.append (tweets_data['user']['screen_name'])
            tweet_csv.append (tweets_data['user']['id'])
            if 'extended_tweet' in tweets_data:
                tweet_csv.append (tweets_data['extended_tweet']['full_text'])
            else:
                tweet_csv.append (tweets_data['text'])
            self.csv_data.append (tweet_csv)

        return True

    '''
    creating data frame with those information
    '''

    def create_dataframe(self):
        self.make_csv_data ()
        self.data_frame = panda.DataFrame (self.csv_data, columns=['name', 'id', 'text'])

    '''
    to get unique user name, this will return a
    dict, which has user name and occurrence.
    '''

    def get_uniq_user_count(self):
        self.create_dataframe ()
        df = self.data_frame.name.value_counts ()
        return df.to_dict ()

    '''
    this function will printout the user related details
    '''

    def print_uniq_user_count(self):
        print ('\n')
        print ('tweet users and tweet count -')
        user_dict = self.get_uniq_user_count ()
        for k, v in user_dict.items ():
            print ('{: >20}{: >20}'.format (k, v))

    '''
    this function will get all the text from existing
    dataframe and then undergoes nlp mechanism.
    '''

    def analyse_words_in_tweets(self):
        valid_string_exp = re.compile ('[0-9a-zA-Z]')
        self.valid_string_pool = []
        self.create_dataframe ()
        data_hash = self.data_frame.to_dict ('records')
        for data_information in data_hash:
            if 'text' in data_information:
                text = data_information['text']
                # this is to skip urls from text
                raw_text = re.sub (r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text, flags=re.MULTILINE)
                tokens = nltk.word_tokenize (raw_text)
                tagged = nltk.pos_tag (tokens)
                for tag in tagged:
                    if tag[1].startswith ('N') or tag[1] == 'FW':
                        if valid_string_exp.search (tag[0]):
                            self.valid_string_pool.append (tag[0].lower ())
        word_dataframe = panda.DataFrame ({'words': self.valid_string_pool})
        self.uniq_words = word_dataframe.words.value_counts ().nlargest (10).to_dict ()

    '''
    this function will printout the top 10 frequent words
    '''

    def print_unique_words(self):
        print ('\n')
        print ('Top 10 frequent words -')
        self.analyse_words_in_tweets ()
        for k, v in self.uniq_words.items ():
            print ('{: >20}{: >20}'.format (k, v))

# if __name__ == '__main__':
#     tweet = TweetProcessor()
#     with open('./twitter_streaming_api/sample_tweet.json') as f:
#         tweet.tweet_data = load(f)
# # tweet.print_uniq_user_count()
# # tweet.print_domain_related_result()
# tweet.print_unique_words()
