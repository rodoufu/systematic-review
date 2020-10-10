import json
import os.path
from cache import SearchCache
from search import SearchRequest, SearchRequestSource
from search_source import SearchSource
from typing import Set, List


class SearchEngine(object):
	def __init__(self, cache_file_name: str = "cache.sr"):
		self.cache_file_name = cache_file_name
		if os.path.exists(self.cache_file_name) and os.path.isfile(self.cache_file_name):
			self.cache = SearchCache.load(self.cache_file_name)
		else:
			self.cache = SearchCache()
		self.sources: List[SearchSource] = []
		self.requests: Set[SearchRequest] = set()

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()

	async def run(self):
		to_wait = []
		for request in self.requests:
			for source in self.sources:
				search_source = SearchRequestSource(request, source.source())
				if search_source not in self.cache:
					to_wait += [(search_source, source.search(request))]

		# async for it in resp:
		# 	self.cache[search_source] = it
		has_new = [True]
		while has_new and all(has_new):
			has_new = []
			for search_source, resp in to_wait:
				try:
					it = await next(resp)
					self.cache[search_source] = it
					has_new.append(True)
				except StopIteration:
					has_new.append(False)
			to_wait = [to_wait[i] for i in range(len(to_wait)) if has_new[i]]

		self.cache.dump(self.cache_file_name)
