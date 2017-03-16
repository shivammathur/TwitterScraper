class SearchParams:
    def __init__(self):
        self.maxTweets = 0

    def set_username(self, username):
        self.username = username
        return self

    def set_since(self, since):
        self.since = since
        return self

    def set_until(self, until):
        self.until = until
        return self

    def set_search(self, query_search):
        self.querySearch = query_search
        return self

    def set_max_tweets(self, max_tweets):
        self.maxTweets = max_tweets
        return self

    def set_top_tweets(self, top_tweets):
        self.topTweets = top_tweets
        return self
