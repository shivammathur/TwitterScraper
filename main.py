from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
import twitter_scraper as twitter_scraper
import json
import codecs
standard_library.install_aliases()


def main():
    def build_list(t, tweet_list):
        tweet_list.append(
            {
                "username": t.username,
                "retweet": t.retweets,
                "tweet": t.text,
                "mentions": t.mentions,
                "hashtags": t.hashtags,
                "date": t.date.__str__()
            }
        )
        return tweet_list

    def print_to_file(data, filename):
        try:
            with codecs.open(filename + '.json', 'a', 'utf-8') as f:
                f.write(data)
                return True
        except BaseException as e:
            print(e)

    search_term = '@meshivammathur'
    search_params = twitter_scraper.scraper.SearchParams().set_username(search_term).set_max_tweets(400)
    tweets = twitter_scraper.scraper.Scraper.get_tweets(search_params)

    t_list = []
    for tweet in tweets:
        t_list = build_list(tweet, t_list)
    json_data = json.dumps(t_list, indent=4)
    print_to_file(json_data, search_term)

if __name__ == '__main__':
    main()
