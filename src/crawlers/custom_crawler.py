from typing import Iterable, List

from .base import fetch_urls, CrawlResult


def crawl_custom(urls: Iterable[str]) -> List[CrawlResult]:
    return fetch_urls(urls)
