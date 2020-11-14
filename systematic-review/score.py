from __future__ import annotations
import abc
from article import Article


class Score(object):
	@abc.abstractmethod
	def calculate_score(self, article: Article) -> int:
		pass
