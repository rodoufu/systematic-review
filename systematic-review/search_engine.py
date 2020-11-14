import json
import logging
import os.path
import time
from article import Article
from cache import SearchCache
from search import SearchRequest, SearchRequestSource
from search_source import SearchSource
from typing import Set, List, Optional, Iterable
from util import get_logger_child


class SearchEngine(object):
	def __init__(
			self, cache_file_name: str = "data/cache.sr", logger: logging.Logger = None,
			ignore_cache: bool = False,
	):
		self.logger = get_logger_child(type(self).__name__, logger)
		self.save_every: Optional[int] = 100
		self.sleep_between_calls_ms: Optional[int] = 100
		self.sources: List[SearchSource] = []
		self.requests: Set[SearchRequest] = set()
		self.compress: bool = True
		self.cache_file_name = cache_file_name
		self.cache: Optional[SearchCache] = None
		self.found_titles: Set[str] = set()
		self.ignore_cache = ignore_cache

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()

	async def run(self):
		self.logger.info(f"Starting requests")
		if self.sources:
			self.logger.info(f"Sources: {[x.source() for x in self.sources]}")
		else:
			self.logger.warning("No source was selected")
		self.logger.info(f"Requests: {[x for x in self.requests]}")

		if not self.cache:
			if os.path.exists(self.cache_file_name) and os.path.isfile(self.cache_file_name):
				self.cache = SearchCache.load(filename=self.cache_file_name, compress=self.compress)
			else:
				self.cache = SearchCache()

		count_articles = 0
		to_wait = []
		for request in self.requests:
			for source in self.sources:
				search_source = SearchRequestSource(request, source.source())
				if self.ignore_cache or search_source not in self.cache:
					to_wait += [(search_source, source.search(request))]
				else:
					self.logger.info(f"Source: {source} is using cache for {request}")
				for author in source.found_authors():
					self.cache.add_author(author)

		def dump():
			self.logger.info(f"Dumping cache of size: {len(self.cache)}")
			self.cache.dump(filename=self.cache_file_name, compress=self.compress)
			self.logger.info(f"Dump finished")

		has_new = [True]
		while has_new and all(has_new):
			self.logger.debug(f"Articles: {count_articles}, requests: {[it for it, _ in to_wait]}")
			has_new = []
			for search_source, resp in to_wait:
				try:
					it = await resp.__anext__()
					self.cache[search_source] = it
					self.found_titles.add(it.article.normalized_title)
					count_articles += 1
					has_new.append(True)

					if self.save_every and count_articles % self.save_every == 0:
						dump()
				except (StopIteration, StopAsyncIteration):
					self.logger.info(f"No more results for {search_source}")
					has_new.append(False)
				except Exception:
					self.logger.exception(f"There was a problem with the iterator for {search_source}")
					has_new.append(False)
			to_wait = [to_wait[i] for i in range(len(to_wait)) if has_new[i]]
			if self.sleep_between_calls_ms:
				time.sleep(self.sleep_between_calls_ms / 1000.0)

		dump()

	def found_articles(self) -> Iterable[Article]:
		for article in self.cache.unique_articles():
			if article.normalized_title in self.found_titles:
				yield article
