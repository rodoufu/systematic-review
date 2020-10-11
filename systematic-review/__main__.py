import argparse
import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from search import SearchRequest, SearchToken
from search_engine import SearchEngine
from search_source import GoogleScholarSearch, IEEESearch


def parse_args():
	parser = argparse.ArgumentParser(description='Systematic review')
	# Log arguments
	parser.add_argument(
		'--log-format', type=str,
		default='%(asctime)s %(levelname)s %(filename)s %(lineno)d "%(name)s" "%(message)s"',
		help='Log format',
	)
	parser.add_argument(
		'-v', '--log-level', default='INFO', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
		help='Log level',
	)

	# Engine arguments
	parser.add_argument(
		'--sleep-between-calls', default=100, help='Time (ms) to sleep between calls'
	)

	# Cache arguments
	parser.add_argument(
		'--cache-save-every', default=1,
		help='Save cache every new requests',
	)
	parser.add_argument('--cache-compress', default=False, help='Compress cache')
	parser.add_argument('--cache-file-name', default='cache.sr', help='Cache file name')
	parser.add_argument(
		'--env-file-name', default=Path('..') / '.env', help='Environment file name',
	)

	parser.add_argument(
		'--source-google-scholar', default=True, help='Use Google Scholar as source',
	)
	parser.add_argument(
		'--google-scholar-use-proxy', default=False, help='Google Scholar should use proxy',
	)
	parser.add_argument(
		'--source-ieee', default=False, help='Use IEEE as source (Requires API key)',
	)

	return parser.parse_args()


async def main():
	args = parse_args()
	load_dotenv(dotenv_path=args.env_file_name)

	logger = logging.getLogger("systematic_review")
	handler = logging.StreamHandler()
	handler.setLevel(args.log_level)
	handler.setFormatter(logging.Formatter(args.log_format))

	logger.addHandler(handler)

	engine = SearchEngine(logger=logger)
	engine.save_every = args.cache_save_every
	engine.compress = args.cache_compress
	engine.cache_file_name = args.cache_file_name
	engine.sleep_between_calls_ms = args.sleep_between_calls

	# if args.source_google_scholar:
	# 	engine.sources.append(GoogleScholarSearch(use_proxy=args.google_scholar_use_proxy))
	if args.source_ieee:
		engine.sources.append(IEEESearch(api_key=os.getenv('IEE_API_KEY')))

	# TODO send terms here
	engine.requests.add(SearchRequest(token=SearchToken.Term, value="BFT"))

	await engine.run()


if __name__ == '__main__':
	# loop = asyncio.get_event_loop()
	# asyncio.set_event_loop(loop)

	# loop.run_until_complete(main())
	asyncio.run(main())
