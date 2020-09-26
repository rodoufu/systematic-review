import unittest
from article import Article
from cache import SearchCache
from search import SearchRequestSource, SearchResponse, SearchRequest, SearchToken
from source import Source


class CacheTest(unittest.TestCase):
	def test_one_source(self):
		cache = SearchCache()
		bft_request = SearchRequest(token=SearchToken.Term, value="BFT")
		bft_request_scopus = SearchRequestSource(request=bft_request, source=Source.Scopus)
		bft_article = Article(title="New BFT", author=["Jose da Silva"])

		self.assertFalse(bft_request_scopus in cache)
		bft_response = SearchResponse(request_source=bft_request_scopus, article=bft_article)
		cache[bft_request_scopus] = bft_response
		self.assertTrue(bft_request_scopus in cache)

		dbft_request = SearchRequest(token=SearchToken.Term, value="dBFT")
		dbft_request_scopus = SearchRequestSource(request=dbft_request, source=Source.Scopus)
		self.assertFalse(dbft_request_scopus in cache)

		dbft_article = Article(title="New dBFT", author=["Jose da Silva"])
		dbft_response = SearchResponse(request_source=dbft_request_scopus, article=dbft_article)
		cache[dbft_request_scopus] = dbft_response
		self.assertTrue(dbft_request_scopus in cache)

		self.assertTrue(bft_request_scopus in cache)


if __name__ == '__main__':
	unittest.main()
