from dataclasses import dataclass
from typing import Iterable, Dict, Any, List

import requests


@dataclass
class CrawlResult:
    url: str
    status_code: int
    text: str
    metadata: Dict[str, Any]


def fetch_urls(urls: Iterable[str], timeout: int = 15) -> List[CrawlResult]:
    results: List[CrawlResult] = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
            results.append(
                CrawlResult(
                    url=url,
                    status_code=resp.status_code,
                    text=resp.text,
                    metadata={"content_type": resp.headers.get("content-type", "")},
                )
            )
        except requests.RequestException as exc:
            results.append(
                CrawlResult(
                    url=url,
                    status_code=0,
                    text="",
                    metadata={"error": str(exc)},
                )
            )
    return results
