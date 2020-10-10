import json
from search import SearchRequest, Source
from typing import Set


class SearchEngine(object):
	def __init__(self):
		self.sources: Set[Source] = set()
		self.requests: Set[SearchRequest] = set()

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()
