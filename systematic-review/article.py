from __future__ import annotations
from typing import List, Optional
import json


class Article(object):
	def __init__(
			self, title: str, author: List[str], year: Optional[int] = None, abstract: Optional[str] = None,
			references: Optional[List[Article]] = None, journal: Optional[str] = None, publisher: Optional[str] = None,
			citations: Optional[int] = None, doi: Optional[int] = None,
	):
		self.title = title.strip()
		self.author = [self.format_text(x) for x in author]
		self.year = year
		self.abstract = self.format_text(abstract)
		self.references = references
		self.journal = self.format_text(journal)
		self.publisher = self.format_text(publisher)
		self.citations = citations
		self.doi = doi

	def format_text(self, text: Optional[str]) -> Optional[str]:
		return text.strip() if text is not None else None

	def __str__(self) -> str:
		return json.dumps(self.__dict__)

	def __repr__(self):
		return self.__str__()
