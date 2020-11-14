from __future__ import annotations
import json
from typing import List, Optional
from util import format_text, normalize_text


class Article(object):
	def __init__(
			self, title: str, author: List[str], year: Optional[int] = None, abstract: Optional[str] = None,
			references: Optional[List[Article]] = None, journal: Optional[str] = None, publisher: Optional[str] = None,
			citations: Optional[int] = None, doi: Optional[str] = None, downloads: Optional[int] = None,
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
		def empty_text(text):
			return not text or len(text.strip()) == 0

		if empty_text(self.title) == 0:
			self.title = other.title
		if empty_text(self.abstract) == 0:
			self.abstract = other.abstract
		if empty_text(self.publisher) == 0:
			self.publisher = other.publisher
		if empty_text(self.journal) == 0:
			self.journal = other.journal
		if empty_text(self.doi) == 0:
			self.doi = other.doi

		if not self.year:
			self.year = other.year
		if not self.citations:
			self.citations = other.citations
		if not self.downloads:
			self.downloads = other.downloads

		# lists
		if not self.author:
			self.author = [x for x in other.author or []]
		if not self.references:
			self.references = [x for x in other.references or []]

		return self
