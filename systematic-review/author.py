from __future__ import annotations
from typing import Optional

from util import normalize_text


class Author(object):
	def __init__(self, name: str, affiliation: Optional[str], citations: Optional[int]):
		self.__name = None
		self.normalized_name = None
		self.name = name
		self.affiliation = affiliation
		self.citations = citations

	@property
	def name(self) -> str:
		return self.__name

	@name.setter
	def name(self, value: str):
		self.__name = value
		self.normalized_name = normalize_text(value)
