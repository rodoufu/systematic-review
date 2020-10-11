from __future__ import annotations
import bz2
import pickle
import json
from article import Article
from search import SearchRequestSource, SearchResponse, SearchRequest
from source import Source
from typing import Dict, NoReturn, Set, Union, Iterable


class SearchCache(object):
	def __init__(self, ignore_case: bool = True):
		self.ignore_case = ignore_case
		self.data: Dict[Source, Dict[SearchRequest, Set[SearchResponse]]] = {}

	def __contains__(self, item: SearchRequestSource) -> bool:
		try:
			return self[item] is not None
		except KeyError:
			return False

	def __check(self, item: SearchRequestSource):
		if item.source not in self.data:
			raise KeyError(f"Source not found: {item.source}")
		if item.request not in self.data[item.source]:
			raise KeyError(f"Request {item.request} not found for source: {item.source}")

	def __getitem__(self, item: SearchRequestSource) -> Set[SearchResponse]:
		if self.ignore_case:
			item.request.value = item.request.value.lower()
		self.__check(item)
		return self.data[item.source][item.request]

	def __setitem__(self, item: SearchRequestSource, value: SearchResponse) -> NoReturn:
		if self.ignore_case:
			item.request.value = item.request.value.lower()
		self.data[item.source] = self.data.get(item.source, {})
		self.data[item.source][item.request] = self.data[item.source].get(item.request, set())
		self.data[item.source][item.request].add(value)

	def __delitem__(self, key: Union[SearchRequestSource, SearchResponse]) -> NoReturn:
		if type(key) is SearchRequestSource:
			if self.ignore_case:
				key.request.value = key.request.value.lower()
			self.__check(key)
			del self.data[key.source][key.request]
		elif type(key) is SearchResponse:
			if self.ignore_case:
				key.request_source.request.value = key.request_source.request.value.lower()
			self.__check(key.request_source)
			obj = self.data[key.request_source.source][key.request_source.request]
			if key not in obj:
				raise KeyError(f"Request {key} not found")
			obj.remove(key)

	def __len__(self) -> int:
		return sum([
			sum([
				len(set_response)
				for set_response in search_request_response.values()
			])
			for search_request_response in self.data.values()
		])

	def dump(self, filename: str, compress: bool = True) -> NoReturn:
		def get_file():
			return bz2.BZ2File(filename, 'w') if compress else open(filename, 'wb')

		with get_file() as out_file:
			pickle.dump(self.__dict__, out_file)

	@staticmethod
	def load(filename: str, compress: bool = True) -> SearchCache:
		def get_file():
			return bz2.BZ2File(filename, 'r') if compress else open(filename, 'rb')

		with get_file() as in_file:
			resp = SearchCache()
			resp.__dict__ = pickle.load(in_file, encoding='bytes')
			return resp

	def __str__(self) -> str:
		return json.dumps(self.__dict__, default=str)

	def __repr__(self):
		return self.__str__()

	def articles(self) -> Iterable[Article]:
		for responses_set in self.data.values():
			for responses in responses_set.values():
				for resp in responses:
					yield resp.article

	def unique_articles(self) -> Iterable[Article]:
		titles = set()
		for it in self.articles():
			if it.normalized_title not in titles:
				titles.add(it.normalized_title)
				yield it
