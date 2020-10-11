from __future__ import annotations
import abc
from article import Article
from typing import AsyncIterable


class Exporter(object):
	@abc.abstractmethod
	async def prefix(self) -> AsyncIterable:
		pass

	@abc.abstractmethod
	async def suffix(self) -> AsyncIterable:
		pass

	@abc.abstractmethod
	async def content(self, article: Article) -> AsyncIterable:
		pass


class CSVExporter(Exporter):
	def __init__(self, separator: str = ';'):
		self.separator = separator

	async def prefix(self) -> AsyncIterable:
		yield f'publisher{self.separator}journal{self.separator}year{self.separator}normalized_title{self.separator}'
		yield f'title{self.separator}doi{self.separator}citations{self.separator}author{self.separator}'
		yield f'references{self.separator}abstract'
		yield f'\n'

	async def suffix(self) -> AsyncIterable:
		yield ''

	async def content(self, article: Article) -> AsyncIterable:
		yield f'{article.publisher}{self.separator}{article.journal}{self.separator}{article.year}{self.separator}'
		yield f'{article.normalized_title}{self.separator}'
		yield f'{article.title}{self.separator}{article.doi}{self.separator}{article.citations}{self.separator}'
		yield f'{article.author}{self.separator}'
		yield f'{article.references}{self.separator}{article.abstract}'
		yield f'\n'
