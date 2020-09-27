from enum import Enum


class Source(Enum):
	GoogleScholar = 1
	Scopus = 2
	IEEE = 3
	PubMed = 4
	Nature = 5
	ResearchGate = 6

	def __str__(self) -> str:
		return self.name

	def __repr__(self):
		return self.__str__()
