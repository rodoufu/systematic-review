import json
import os.path
import time
from cache import SearchCache
from search import SearchRequest, SearchRequestSource
from search_source import SearchSource
from typing import Set, List, Optional


class SearchEngine(object):
	def __init__(self, cache_file_name: str = "cache.sr"):
		self.save_every: Optional[int] = 100
		self.sleep_between_calls_ms: Optional[int] = 100
		self.sources: List[SearchSource] = []
		self.requests: Set[SearchRequest] = set()
		self.cache_file_name = cache_file_name
		if os.path.exists(self.cache_file_name) and os.path.isfile(self.cache_file_name):
			self.cache = SearchCache.load(self.cache_file_name)
		else:
			self.cache = SearchCache()

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()

	async def run(self):
		count_articles = 0
		to_wait = []
		for request in self.requests:
			for source in self.sources:
				search_source = SearchRequestSource(request, source.source())
				if search_source not in self.cache:
					to_wait += [(search_source, source.search(request))]

		has_new = [True]
		while has_new and all(has_new):
			has_new = []
			for search_source, resp in to_wait:
				try:
					it = await resp.__anext__()
					self.cache[search_source] = it
					count_articles += 1
					has_new.append(True)

					if self.save_every and count_articles % self.save_every == 0:
						self.cache.dump(self.cache_file_name)
				except StopIteration:
					has_new.append(False)
			to_wait = [to_wait[i] for i in range(len(to_wait)) if has_new[i]]
			if self.sleep_between_calls_ms:
				time.sleep(self.sleep_between_calls_ms)

		self.cache.dump(self.cache_file_name)
