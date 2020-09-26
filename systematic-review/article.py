from __future__ import annotations
from typing import List, Optional


class Article(object):
	def __init__(
			self, title: str, author: List[str], year: Optional[int] = None, abstract: Optional[str] = None,
			references: Optional[List[Article]] = None,
	):
		self.title = title
		self.author = author
		self.year = year
		self.abstract = abstract
		self.references = references
