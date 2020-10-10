import unittest
from util import rm_diacritics, rm_diacritics_char


class UtilTest(unittest.TestCase):
	def test_remove_accents_char(self):
		self.assertEqual("a", rm_diacritics_char("á"))
		self.assertEqual("c", rm_diacritics_char("ç"))

	def test_remove_accents(self):
		self.assertEqual("agua", rm_diacritics("água"))
		self.assertEqual("cachaca", rm_diacritics("cachaça"))


if __name__ == '__main__':
	unittest.main()
