from __future__ import annotations
import abc
import json
import urllib.parse
from article import Article
from typing import Iterable, Dict, AsyncIterable
from scholarly import scholarly, ProxyGenerator
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
from aiohttp import ClientSession
from search import SearchRequest, SearchResponse, SearchToken, SearchRequestSource, Source


class SearchSource(object):
	@abc.abstractmethod
	async def search(self, request: SearchRequest) -> AsyncIterable[SearchResponse]:
		pass

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()

	@abc.abstractmethod
	def source(self) -> Source:
		pass


class GoogleScholarSearch(SearchSource):
	__is_using_proxy = False

	def __init__(self, use_proxy: bool = True):
		if use_proxy and not GoogleScholarSearch.__is_using_proxy:
			pg = ProxyGenerator()
			pg.FreeProxies()
			scholarly.use_proxy(pg)
			GoogleScholarSearch.__is_using_proxy = True

	async def search(self, request: SearchRequest) -> AsyncIterable[SearchResponse]:
		def process_publication(pub) -> Iterable[SearchResponse]:
			pub.fill()
			yield SearchResponse(
				request_source=SearchRequestSource(
					request=request,
					source=Source.GoogleScholar,
				),
				article=Article(
					title=pub.bib.get('title'),
					author=pub.bib['author'].split('and') if 'author' in pub.bib else [],
					year=int(pub.bib['year']) if 'year' in pub.bib else None,
					abstract=pub.bib.get('abstract'),
					journal=pub.bib.get('journal'),
					publisher=pub.bib.get('publisher'),
					citations=int(pub.bib['cites']) if 'cites' in pub.bib else None,
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

	def source(self) -> Source:
		return Source.GoogleScholar


class ScopusSearch(SearchSource):
	def __init__(self, config_file_name: str = "config.json"):
		with open(config_file_name) as con_file:
			config = json.load(con_file)
			self.client = ElsClient(config['apikey'])
			if 'insttoken' in config:
				self.client.inst_token = config['insttoken']

	async def search(self, request: SearchRequest) -> AsyncIterable[SearchResponse]:
		if request.token == SearchToken.Author:
			auth_srch = ElsSearch(f'authlast({request.value.split(" ")[-1]})', 'author')
			auth_srch.execute(self.client)
			print(f"{auth_srch}")
			yield SearchResponse(
				request_source=SearchRequestSource(
					request=request,
					source=Source.Scopus,
				),
				article=Article(
					title="pub.bib.get('title')",
					author=["pub.bib['author'].split('and') if 'author' in pub.bib else []"],
					year=0,  # int(pub.bib['year']) if 'year' in pub.bib else None,
					abstract="pub.bib.get('abstract')",
					journal="pub.bib.get('journal')",
					publisher="pub.bib.get('publisher')",
				),
				raw=1,  # auth_srch,
			)
		elif request.token == SearchToken.Term:
			pass
		elif request.token == SearchToken.Title:
			pass

	def source(self) -> Source:
		return Source.Scopus


class IEEESearch(SearchSource):
	def __init__(self, api_key: str):
		self.api_key = api_key
		self.api_version = 'v1'
		self.protocol = 'https'

	def get_url(self, params: Dict[str, object] = None, max_records: int = 50, start_record: int = 1) -> str:
		if not params:
			params = {}
		# http://ieeexploreapi.ieee.org/api/v1/search/articles?apikey=8ne98h79n4j299yw79dx96bn&format=xml&max_records=25&start_record=1&sort_order=asc&sort_field=article_number&author=Rodolfo+Pereira+Araujo
		params['apikey'] = self.api_key
		params['format'] = 'json'
		params['max_records'] = max_records
		params['sort_order'] = 'asc'
		params['sort_field'] = 'article_title'
		params['start_record'] = start_record

		def to_url(param, value):
			return f"{to_url(param, value)}"

		params_str = '&'.join(
			[f"{urllib.parse.quote(str(param))}={urllib.parse.quote(str(value))}" for param, value in params.items()])
		return f"{self.protocol}://ieeexploreapi.ieee.org/api/{self.api_version}/search/articles?{params_str}"

	async def get_all_resources(
			self, request: SearchRequest, params: Dict[str, object], max_records: int = 50,
	) -> AsyncIterable[SearchResponse]:
		def create_search_response(article) -> SearchResponse:
			return SearchResponse(
				request_source=SearchRequestSource(
					request=request,
					source=Source.Scopus,
				),
				article=Article(
					title=article.get('title'),
					author=[
						author.get('full_name') for author in article.get('authors', {}).get('authors', [])
					],
					year=article.get('publication_year'),
					abstract=article.get('abstract'),
					journal=article.get('publication_title'),
					publisher=article.get('publisher'),
					citations=article.get('citing_paper_count', 0) + article.get('citing_patent_count', 0),
					doi=article.get('doi'),
				),
				raw=article,
			)

		async def next_page(start_record=1) -> AsyncIterable[SearchResponse]:
			async with ClientSession() as session:
				url = self.get_url(params=params, max_records=max_records, start_record=start_record)
				async with session.get(url=url) as response:
					result = await response.json()
					total_records = result.get('total_records', 0)
					articles = result.get('articles')
					if result and total_records > 0 or articles:
						for article in articles:
							yield create_search_response(article)
						if total_records > max_records and start_record < total_records:
							async for it in next_page(start_record + max_records):
								yield it

		async for it in next_page():
			yield it

	async def search(self, request: SearchRequest) -> AsyncIterable[SearchResponse]:
		if request.token == SearchToken.Author:
			async for it in self.get_all_resources(request=request, params={'author': request.value}):
				yield it
		elif request.token == SearchToken.Term:
			async for it in self.get_all_resources(request=request, params={'index_terms': request.value}):
				yield it
			async for it in self.get_all_resources(request=request, params={'abstract': request.value}):
				yield it
		elif request.token == SearchToken.Title:
			async for it in self.get_all_resources(request=request, params={'article_title': request.value}):
				yield it

	def source(self) -> Source:
		return Source.IEEE
