import abc
import json
from article import Article
from typing import Iterable
from scholarly import scholarly, ProxyGenerator

from search import SearchRequest, SearchResponse, SearchToken, SearchRequestSource, Source


class SearchSource(object):
	@abc.abstractmethod
	def search(self, request: SearchRequest) -> Iterable[SearchResponse]:
		return iter(())

	def __str__(self) -> str:
		return json.dumps(self.__dict__, default=str)


class GoogleScholarSearch(object):
	__is_using_proxy = False

	def __init__(self, use_proxy: bool = True):
		if use_proxy and not GoogleScholarSearch.__is_using_proxy:
			pg = ProxyGenerator()
			pg.FreeProxies()
			scholarly.use_proxy(pg)
			GoogleScholarSearch.__is_using_proxy = True

	def search(self, request: SearchRequest) -> Iterable[SearchResponse]:
		def process_publication(pub) -> Iterable[SearchResponse]:
			pub.fill()
			yield SearchResponse(
				request_source=SearchRequestSource(
					request=request, source=Source.GoogleScholar,
				),
				article=Article(
					title=pub.bib.get('title'),
					author=pub.bib['author'].split('and') if 'author' in pub.bib else [],
					year=int(pub.bib['year']) if 'year' in pub.bib else None,
					abstract=pub.bib.get('abstract'),
					journal=pub.bib.get('journal'),
					publisher=pub.bib.get('publisher'),
				),
				raw=pub,
			)

		def process_author(author) -> Iterable[SearchResponse]:
			author.fill()
			for pub in author.publications:
				for it in process_publication(pub):
					yield it

		if request.token == SearchToken.Author:
			for author in scholarly.search_author(request.value):
				for it in process_author(author):
					yield it
		elif request.token == SearchToken.Term:
			for author in scholarly.search_keyword(request.value):
				for it in process_author(author):
					yield it
		elif request.token == SearchToken.Title:
			for pub in scholarly.search_pubs(request.value):
				for it in process_publication(pub):
					yield it
