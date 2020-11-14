import logging
import re
import unicodedata as ud
from typing import Optional


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


def get_logger_child(name: str, logger: logging.Logger = None) -> logging.Logger:
	if logger:
		return logger.getChild(name)
	else:
		return logging.getLogger(name)


def format_text(text: Optional[str]) -> Optional[str]:
	return re.sub(' +', ' ', text.strip().replace('\n', ' ')) if text is not None else None
