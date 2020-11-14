from __future__ import annotations
import abc
from typing import Union, Optional
from article import Article
from author import Author
from cache import SearchCache


class Score(object):
	def calculate_score(self, obj: Union[Article, Author]) -> int:
		if type(obj) is Article:
			return self._calculate_article_score(obj)
		elif type(obj) is Author:
			return self._calculate_author_score(obj)
		else:
			raise TypeError(f"The type {type(obj)} is not expected")

	@abc.abstractmethod
	def _calculate_author_score(self, author: Author) -> int:
		raise NotImplementedError()

	@abc.abstractmethod
	def _calculate_article_score(self, article: Article) -> int:
		raise NotImplementedError()


class CitationScore(Score):
	@abc.abstractmethod
	def _calculate_author_score(self, author: Author) -> int:
		return author.citations

	@abc.abstractmethod
	def _calculate_article_score(self, article: Article) -> int:
		return article.citations


class HIndexScore(Score):
	def __init__(self, cache: Optional[SearchCache]):
		self.cache = cache

	@abc.abstractmethod
	def _calculate_author_score(self, author: Author) -> int:
		return author.h_index

	@abc.abstractmethod
	def _calculate_article_score(self, article: Article) -> int:
		if not self.cache:
			raise NotImplementedError()
		return max(map(lambda x: x.h_index if x else 0, [
			self.cache.find_author(author_name)
			for author_name in article.author
		]))


class I10IndexScore(Score):
	def __init__(self, cache: Optional[SearchCache]):
		self.cache = cache

	@abc.abstractmethod
	def _calculate_author_score(self, author: Author) -> int:
		return author.i10_index

	@abc.abstractmethod
	def _calculate_article_score(self, article: Article) -> int:
		if not self.cache:
			raise NotImplementedError()
		return max(map(lambda x: x.i10_index if x else 0, [
			self.cache.find_author(author_name)
			for author_name in article.author
		]))

