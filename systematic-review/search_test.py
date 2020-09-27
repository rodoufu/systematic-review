import unittest
from search import SearchRequest, SearchToken


class SearchRequestTest(unittest.TestCase):
	def test_str(self):
		request = SearchRequest(SearchToken.Author, "Barbara Liskov")
		to_str = f"{request}"
		print(f"{to_str}")
		self.assertTrue("Barbara" in to_str)
		self.assertTrue("Liskov" in to_str)


if __name__ == '__main__':
	unittest.main()
