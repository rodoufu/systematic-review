import unittest
import os
from pathlib import Path

from dotenv import load_dotenv


class AppTest(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(AppTest, self).__init__(*args, **kwargs)
		load_dotenv(dotenv_path=Path('..') / '.env')

	def test_env(self):
		self.assertEqual(os.getenv('TEST'), 'test')


if __name__ == '__main__':
	unittest.main()
