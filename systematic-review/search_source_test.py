import unittest

from search_source import GoogleScholarSearch

from search import SearchRequest, SearchToken


class GoogleScholarSearchTest(unittest.TestCase):
	def __init__(self, method_name='runTest'):
		super().__init__(methodName=method_name)
		self.search_source = GoogleScholarSearch(False)

	def test_author(self):
		articles = list(self.search_source.search(SearchRequest(SearchToken.Author, "Rodolfo Pereira Araujo")))
		print(f"Articles: {articles}")
		self.assertTrue(len(articles) > 0)


if __name__ == '__main__':
	unittest.main()
