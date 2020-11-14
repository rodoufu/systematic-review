from __future__ import annotations
from typing import Optional, List

from util import normalize_text, format_text, empty_text


class Author(object):
	def __init__(
			self, name: str, affiliation: Optional[str], citations: Optional[int], interests: List[str] = None,
			h_index: Optional[int] = None, i10_index: Optional[int] = None,
	):
		self.__name = None
		self.normalized_name = None
		self.name = name
		self.affiliation = affiliation
		self.citations = citations
		self.interests = [format_text(x) for x in interests or []]
		self.h_index = h_index
		self.i10_index = i10_index

	@property
	def name(self) -> str:
		return self.__name

	@name.setter
	def name(self, value: str):
		self.__name = value
		self.normalized_name = normalize_text(value)

	def merge(self, other: Author) -> Author:
		if empty_text(self.affiliation):
			self.affiliation = other.affiliation

		self.citations = self.citations or other.citations
		self.h_index = self.h_index or other.h_index
		self.i10_index = self.i10_index or other.i10_index

		self.interests = [x for x in self.interests or other.interests or []]

		return self
