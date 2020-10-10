from __future__ import annotations
import json
import string
from typing import List, Optional

from util import rm_diacritics


class Article(object):
	def __init__(
			self, title: str, author: List[str], year: Optional[int] = None, abstract: Optional[str] = None,
			references: Optional[List[Article]] = None, journal: Optional[str] = None, publisher: Optional[str] = None,
			citations: Optional[int] = None, doi: Optional[int] = None,
	):
		self.__title = title.strip()
		self.normalized_title = self.title
		self.author = [self.format_text(x) for x in author]
		self.year = year
		self.abstract = self.format_text(abstract)
		self.references = references
		self.journal = self.format_text(journal)
		self.publisher = self.format_text(publisher)
		self.citations = citations
		self.doi = doi

	@property
	def title(self) -> str:
		return self.__title

	@title.setter
	def title(self, value: str):
		self.__title = value
		self.normalized_title = rm_diacritics(value.strip().lower()).translate(
			str.maketrans('', '', string.punctuation)
		)

	def format_text(self, text: Optional[str]) -> Optional[str]:
		return text.strip() if text is not None else None

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash(self.normalized_title)

	def __eq__(self, other):
		return type(other) is Article and self.normalized_title == other.normalized_title
