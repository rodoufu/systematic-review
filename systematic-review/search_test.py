import unittest
from article import Article
from search import SearchRequest, SearchToken, SearchResponse, SearchRequestSource, Source


class SearchRequestTest(unittest.TestCase):
	def test_str(self):
		request = SearchRequest(SearchToken.Author, "Barbara Liskov")
		to_str = f"{request}"
		print(f"{to_str}")
		self.assertTrue("Barbara" in to_str)
		self.assertTrue("Liskov" in to_str)


class SearchResponseTest(unittest.TestCase):
	def test_str(self):
		bft_request = SearchRequest(token=SearchToken.Term, value="BFT")
		bft_request_scopus = SearchRequestSource(request=bft_request, source=Source.Scopus)
		bft_article = Article(title="New BFT", author=["Jose da Silva"])

		bft_response = SearchResponse(request_source=bft_request_scopus, article=bft_article)
		to_str = f"{bft_response}"
		print(f"{to_str}")
		self.assertTrue("Jose" in to_str)
		self.assertTrue("Silva" in to_str)

		list_to_str = f"{[bft_response]}"
		print(f"{list_to_str}")
		self.assertTrue("Jose" in list_to_str)
		self.assertTrue("Silva" in list_to_str)


if __name__ == '__main__':
	unittest.main()
