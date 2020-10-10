import unicodedata as ud


def rm_diacritics_char(char):
	"""
	Return the base character of char, by "removing" any
	diacritics like accents or curls and strokes and the like.
	"""
	desc = ud.name(char)
	cutoff = desc.find(' WITH ')
	if cutoff != -1:
		desc = desc[:cutoff]
		try:
			char = ud.lookup(desc)
		except KeyError:
			pass  # removing "WITH ..." produced an invalid name
	return char


def rm_diacritics(text: str):
	return "".join([rm_diacritics_char(x) for x in text])
