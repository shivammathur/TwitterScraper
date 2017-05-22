from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
class SearchParams(object):
	
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
	
	def set_lang(self, Lang):
		self.lang = Lang
		return self