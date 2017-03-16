import twitter_scraper
import json


def main():
    def build_list(t, tweet_list):
        tweet_list.append(
            {
                "username": t.username,
                "tweet": t.retweets,
                "retweets": t.text,
                "mentions": t.mentions,
                "hashtags": t.hashtags
            }
        )
        return tweet_list

    def print_to_file(data, filename):
        try:
            with open(filename + '.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print e

    search_term = '#earthquake'
    search_params = twitter_scraper.scraper.SearchParams().set_search(search_term).set_since("2017-02-01").set_until(
        "2017-03-01")
    tweets = twitter_scraper.scraper.Scraper.get_tweets(search_params)

    t_list = []
    for tweet in tweets:
        t_list = build_list(tweet, t_list)
    json_data = json.dumps(t_list, indent=4)
    print_to_file(json_data, search_term)

if __name__ == '__main__':
    main()
