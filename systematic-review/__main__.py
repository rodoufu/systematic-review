import argparse
import asyncio
import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from article import Article
from cache import SearchCache
from exporter import CSVExporter
from search import SearchRequest, SearchToken
from search_engine import SearchEngine
from search_source import GoogleScholarSearch, IEEESearch, ACMSearch


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
	parser.add_argument('--list-articles', default=False, help='List the articles found', action="store_true")
	# Searches
	parser.add_argument('--term', action='append', help='Search terms')
	parser.add_argument('--title', action='append', help='Search titles')
	parser.add_argument('--author', action='append', help='Search titles')

	# Cache arguments
	parser.add_argument(
		'--cache-save-every', default=10, help='Save cache every new requests',
	)
	parser.add_argument('--cache-compress', default=False, help='Compress cache', action="store_true")
	parser.add_argument('--cache-file-name', default='cache.sr', help='Cache file name')
	parser.add_argument(
		'--env-file-name', default=Path('..') / '.env', help='Environment file name',
	)
	parser.add_argument('--compact-cache-file', help='Create a compacted cache file')
	parser.add_argument('--cache-searches', default=False, help='Print searches in the cache', action="store_true")
	parser.add_argument('--cache-sources', default=False, help='Print sources in the cache', action="store_true")
	parser.add_argument('--cache-list', default=False, help='List the articles in the cache', action="store_true")

	# Sources
	parser.add_argument(
		'--source-google-scholar', default=False, help='Use Google Scholar as source',
	)
	parser.add_argument(
		'--google-scholar-use-proxy', default=False, help='Google Scholar should use proxy', action="store_true",
	)
	parser.add_argument(
		'--source-ieee', default=False, help='Use IEEE as source (Requires API key)', action="store_true",
	)
	parser.add_argument(
		'--source-acm', default=False, help='Use ACM as source', action="store_true",
	)

	# Exporters
	parser.add_argument('--export-csv', help='Filename for the CSV exporter')

	return parser.parse_args()


def article_simple_print(logger: logging.Logger, article: Article):
	authors = f"{article.author}" if len(article.author) <= 3 else f"{article.author[:1] + ['et al']}"
	logger.info(
		f"Publisher: {article.publisher}, Journal: {article.journal}, title: {article.title},"
		f" authors: {authors}"
	)


def build_search_engine(logger: logging.Logger, args) -> Optional[SearchEngine]:
	engine = SearchEngine(logger=logger)
	engine.save_every = args.cache_save_every
	engine.compress = args.cache_compress
	engine.cache_file_name = args.cache_file_name
	engine.sleep_between_calls_ms = args.sleep_between_calls

	if args.source_google_scholar:
		engine.sources.append(GoogleScholarSearch(use_proxy=args.google_scholar_use_proxy))
	if args.source_ieee:
		ieee_api_key = os.getenv('IEE_API_KEY')
		if not ieee_api_key:
			logger.critical("Application is missing IEEE API key")
			return
		engine.sources.append(IEEESearch(api_key=ieee_api_key))
	if args.source_acm:
		engine.sources.append(ACMSearch())

	for term in args.term or []:
		engine.requests.add(SearchRequest(token=SearchToken.Term, value=term))
	for author in args.author or []:
		engine.requests.add(SearchRequest(token=SearchToken.Author, value=author))
	for title in args.title or []:
		engine.requests.add(SearchRequest(token=SearchToken.Title, value=title))

	return engine


async def main():
	args = parse_args()
	load_dotenv(dotenv_path=args.env_file_name)

	logger = logging.getLogger("systematic_review")
	handler = logging.StreamHandler()
	handler.setLevel(args.log_level)
	handler.setFormatter(logging.Formatter(args.log_format))
	logger.addHandler(handler)

	engine = build_search_engine(logger, args)
	if not engine:
		return -1

	await engine.run()
	await generate_output(args, engine, logger)

	if args.compact_cache_file:
		logger.info(f"Compressing {args.cache_file_name} into {args.compact_cache_file}")
		cache = SearchCache.load(args.cache_file_name, compress=False)
		cache.dump(args.compact_cache_file, compress=True)

	return 0


async def generate_output(args, engine: SearchEngine, logger: logging.Logger):
	if args.list_articles:
		for article in engine.found_articles():
			article_simple_print(logger, article)
	logger.info(f"Found {len(engine.found_titles)} articles")

	if args.cache_list:
		count_unique = 0
		for article in engine.cache.unique_articles():
			count_unique += 1
			article_simple_print(logger, article)
		logger.info(f"{count_unique} unique articles in the cache")
	logger.info(f"{len(engine.cache)} articles in the cache")

	exporters = [
		(args.export_csv, CSVExporter(';'))
	]
	for file_name, exporter in exporters:
		if file_name:
			with open(file_name, 'x') as export_csv:
				async for it in exporter.prefix():
					export_csv.write(it)
				for article in engine.cache.unique_articles():
					async for it in exporter.content(article):
						export_csv.write(it)
				async for it in exporter.suffix():
					export_csv.write(it)

	if args.cache_searches:
		logger.info(f"Searches:")
		for search in engine.cache.search_requests():
			logger.info(f"{search.token}: {search.value}")

	if args.cache_sources:
		logger.info(f"Sources:")
		for source in engine.cache.sources():
			logger.info(f"{source}")


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	asyncio.set_event_loop(loop)

	loop.run_until_complete(main())
