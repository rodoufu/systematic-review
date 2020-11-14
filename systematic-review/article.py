from __future__ import annotations
import json
from typing import List, Optional
from util import format_text, normalize_text, empty_text


class Article(object):
	def __init__(
			self, title: str, author: List[str], year: Optional[int] = None, abstract: Optional[str] = None,
			references: List[Article] = None, journal: Optional[str] = None, publisher: Optional[str] = None,
			citations: Optional[int] = None, doi: Optional[str] = None, downloads: Optional[int] = None,
			key_words: List[str] = None,
	):
		self.__title = None
		self.normalized_title = None
		self.title = title
		self.author = [format_text(x) for x in author]
		self.year = year
		self.abstract = format_text(abstract)
		self.references = references or []
		self.journal = format_text(journal)
		self.publisher = format_text(publisher)
		self.citations = citations
		self.doi = doi
		self.downloads = downloads
		self.key_words = [format_text(x) for x in key_words or []]

	@property
	def title(self) -> str:
		return self.__title

	@title.setter
	def title(self, value: str):
		self.__title = value
		self.normalized_title = normalize_text(value)

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash(self.normalized_title)

	def __eq__(self, other):
		return type(other) is Article and self.normalized_title == other.normalized_title

	def merge(self, other: Article) -> Article:
		if empty_text(self.title):
			self.title = other.title
		if empty_text(self.abstract):
			self.abstract = other.abstract
		if empty_text(self.publisher):
			self.publisher = other.publisher
		if empty_text(self.journal):
			self.journal = other.journal
		if empty_text(self.doi):
			self.doi = other.doi

		self.year = self.year or other.year
		self.citations = self.citations or other.citations
		self.downloads = self.downloads or other.downloads

		# lists
		self.author = [x for x in self.author or other.author or []]
		self.references = [x for x in self.references or other.references or []]
		self.key_words = [x for x in self.key_words or other.key_words or []]

		return self
