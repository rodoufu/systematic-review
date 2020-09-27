from enum import Enum
from typing import Set
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


class SearchRequestSource(object):
	def __init__(self, request: SearchRequest, source: Source):
		self.request = request
		self.source = source

	def __str__(self) -> str:
		return json.dumps(self.__dict__, default=str)

	def __repr__(self):
		return self.__str__()


class SearchResponse(object):
	def __init__(self, request_source: SearchRequestSource, article: Article, raw: object = object()):
		self.request_source = request_source
		self.article = article
		self.raw = raw

	def __str__(self) -> str:
		return json.dumps(self.__dict__, default=str)

	def __repr__(self):
		return self.__str__()


class SearchEngine(object):
	def __init__(self):
		self.sources: Set[Source] = set()
		self.requests: Set[SearchRequest] = set()

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()
