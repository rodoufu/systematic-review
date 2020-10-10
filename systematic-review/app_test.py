import asyncio
import os
import unittest
from pathlib import Path
from dotenv import load_dotenv

from search import SearchRequest, SearchToken
from search_engine import SearchEngine

from search_source import GoogleScholarSearch

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)


class AppTest(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(AppTest, self).__init__(*args, **kwargs)
		load_dotenv(dotenv_path=Path('..') / '.env')

	def test_env(self):
		self.assertEqual(os.getenv('TEST'), 'test')

	def test_google_scholar(self):
		engine = SearchEngine()
		engine.sources.append(GoogleScholarSearch(use_proxy=False))
		engine.requests.add(SearchRequest(token=SearchToken.Term, value="BFT"))

		async def the_test():
			await engine.run()
			print(f"cache: {engine}")

		loop.run_until_complete(the_test())


if __name__ == '__main__':
	unittest.main()
