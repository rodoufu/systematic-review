from enum import Enum
from article import Article
from source import Source


class SearchToken(Enum):
	Author = 1
	Title = 2
	Term = 3


class SearchRequest(object):
	def __init__(self, token: SearchToken, value: str):
		self.token = token
		self.value = value


class SearchRequestSource(object):
	def __init__(self, request: SearchRequest, source: Source):
		self.request = request
		self.source = source


class SearchResponse(object):
	def __init__(self, request_source: SearchRequestSource, article: Article, raw: object = object()):
		self.request_source = request_source
		self.article = article
		self.raw = raw
