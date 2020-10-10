from enum import Enum
from article import Article
from source import Source
import json


class SearchToken(Enum):
	Author = 1
	Title = 2
	Term = 3

	def __str__(self) -> str:
		return self.name

	def __repr__(self):
		return self.__str__()


class SearchRequest(object):
	def __init__(self, token: SearchToken, value: str):
		self.token = token
		self.value = value

	def __str__(self) -> str:
		return json.dumps(self.__dict__, default=str)

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash(self.token) + hash(self.value)

	def __eq__(self, other):
		return type(other) is SearchRequest and self.token == other.token and self.value == other.value


class SearchRequestSource(object):
	def __init__(self, request: SearchRequest, source: Source):
		self.request = request
		self.source = source

	def __str__(self) -> str:
		return json.dumps(self.__dict__, default=str)

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash(self.request) + hash(self.source)

	def __eq__(self, other):
		return type(other) is SearchRequestSource and self.request == other.request and self.source == other.source


class SearchResponse(object):
	def __init__(self, request_source: SearchRequestSource, article: Article, raw: object = object()):
		self.request_source = request_source
		self.article = article
		self.raw = raw

	def __str__(self) -> str:
		return json.dumps(self.__dict__, default=str)

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash(self.request_source) + hash(self.article)

	def __eq__(self, other):
		return type(other) is SearchResponse and \
			self.request_source == other.request_source and self.article == other.article
