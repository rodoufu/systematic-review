import unittest
import asyncio

from search_source import GoogleScholarSearch, ScopusSearch, IEEESearch, ACMSearch

from search import SearchRequest, SearchToken

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)


class GoogleScholarSearchTest(unittest.TestCase):
	def __init__(self, method_name='runTest'):
		super().__init__(methodName=method_name)
		self.search_source = GoogleScholarSearch(False)

	def test_author(self):
		async def the_test():
			articles = []
			async for article in self.search_source.search(SearchRequest(SearchToken.Author, "Rodolfo Pereira Araujo")):
				articles.append(article)
			print(f"Articles: {articles}")
			self.assertTrue(len(articles) > 0)

		loop.run_until_complete(the_test())


class ScopusSearchTest(unittest.TestCase):
	def __init__(self, method_name='runTest'):
		super().__init__(methodName=method_name)
		self.search_source = ScopusSearch()

	def test_author(self):
		pass
# articles = list(self.search_source.search(SearchRequest(SearchToken.Author, "Rodolfo Pereira Araujo")))
# print(f"Articles: {articles}")
# self.assertTrue(len(articles) > 0)


class IEEESearchTest(unittest.TestCase):
	def __init__(self, method_name='runTest'):
		super().__init__(methodName=method_name)
		self.search_source = IEEESearch(api_key='123')
		self.search_source.protocol = "http"

	def test_get_url(self):
		url = "http://ieeexploreapi.ieee.org/api/v1/search/articles?apikey=123&format=json&max_records=50&sort_order=asc&sort_field=article_title&start_record=1"
		get_url = self.search_source.get_url()
		self.assertEqual(url, get_url)


class ACMSearchTest(unittest.TestCase):
	def __init__(self, method_name='runTest'):
		super().__init__(methodName=method_name)
		self.search_source = ACMSearch()

	def test_title_bft(self):
		async def the_test():
			async for response in self.search_source.search(SearchRequest(SearchToken.Title, "bft")):
				print(f"response: {response}")

		loop.run_until_complete(the_test())


if __name__ == '__main__':
	unittest.main()
