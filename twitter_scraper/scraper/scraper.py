import urllib
import urllib2
import json
import re
import datetime
import sys
import cookielib
from pyquery import PyQuery
from .. import tweet


class Scraper:
    def __init__(self):
        pass

    @staticmethod
    def get_tweets(search_params, receive_buffer=None, buffer_length=100):
        refresh_cursor = ''

        results = []
        results_aux = []
        cookie_jar = cookielib.CookieJar()

        if hasattr(search_params, 'username') and (
                    search_params.username.startswith("\'") or search_params.username.startswith("\"")) and (
                    search_params.username.endswith("\'") or search_params.username.endswith("\"")
        ):
            search_params.username = search_params.username[1:-1]

        active = True

        while active:
            json_response = Scraper.get_json_response(search_params, refresh_cursor, cookie_jar)
            if len(json_response['items_html'].strip()) == 0:
                break

            refresh_cursor = json_response['min_position']
            tweets = PyQuery(json_response['items_html'])('div.js-stream-tweet')

            if len(tweets) == 0:
                break

            for tweetHTML in tweets:
                tweet_pq = PyQuery(tweetHTML)
                tweet_object = tweet.Tweet()

                username_tweet = tweet_pq("span.username.js-action-profile-name b").text()
                txt = re.sub(r"\s+", " ", tweet_pq("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
                retweets = int(tweet_pq("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr(
                    "data-tweet-stat-count").replace(",", ""))
                favorites = int(tweet_pq("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr(
                    "data-tweet-stat-count").replace(",", ""))
                date_sec = int(tweet_pq("small.time span.js-short-timestamp").attr("data-time"))
                tweet_id = tweet_pq.attr("data-tweet-id")
                permalink = tweet_pq.attr("data-permalink-path")

                geo = ''
                geo_span = tweet_pq('span.Tweet-geo')
                if len(geo_span) > 0:
                    geo = geo_span.attr('title')

                tweet_object.id = tweet_id
                tweet_object.permalink = 'https://twitter.com' + permalink
                tweet_object.username = username_tweet
                tweet_object.text = txt
                tweet_object.date = datetime.datetime.fromtimestamp(date_sec)
                tweet_object.retweets = retweets
                tweet_object.favorites = favorites
                tweet_object.mentions = " ".join(re.compile('(@\\w*)').findall(tweet_object.text))
                tweet_object.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet_object.text))
                tweet_object.geo = geo

                results.append(tweet_object)
                results_aux.append(tweet_object)

                if receive_buffer and len(results_aux) >= buffer_length:
                    receive_buffer(results_aux)
                    results_aux = []

                if 0 < search_params.maxTweets <= len(results):
                    active = False
                    break

        if receive_buffer and len(results_aux) > 0:
            receive_buffer(results_aux)

        return results

    @staticmethod
    def get_json_response(search_params, refresh_cursor, cookie_jar):
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

        url_get_data = ''
        if hasattr(search_params, 'username'):
            url_get_data += ' from:' + search_params.username

        if hasattr(search_params, 'since'):
            url_get_data += ' since:' + search_params.since

        if hasattr(search_params, 'until'):
            url_get_data += ' until:' + search_params.until

        if hasattr(search_params, 'querySearch'):
            url_get_data += ' ' + search_params.querySearch

        if hasattr(search_params, 'topTweets'):
            if search_params.topTweets:
                url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"

        url %= (urllib.quote(url_get_data), refresh_cursor)

        headers = [
            ('Host', "twitter.com"),
            ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
            ('Accept', "application/json, text/javascript, */*; q=0.01"),
            ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
            ('X-Requested-With', "XMLHttpRequest"),
            ('Referer', url),
            ('Connection', "keep-alive")
        ]

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            json_response = response.read()
        except:
            print "url: https://twitter.com/search?q=%s&src=typd" % urllib.quote(url_get_data)
            sys.exit()

        json_data = json.loads(json_response)

        return json_data
