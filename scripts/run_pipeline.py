from pathlib import Path
from typing import Dict, Any, List

import yaml

from src.crawlers.custom_crawler import crawl_custom
from src.crawlers.filings_crawler import crawl_filings
from src.crawlers.news_crawler import crawl_news
from src.parsers.html_parser import extract_text
from src.reports.generate import build_report
from src.signals.extract import extract_signals
from src.summarizers.basic import summarize_text
from src.storage.local_store import write_jsonl, write_text


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "src" / "config"
DATA_DIR = ROOT / "data"


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def crawl_by_type(source_type: str, urls: List[str]):
    if source_type == "news":
        return crawl_news(urls)
    if source_type == "filings":
        return crawl_filings(urls)
    return crawl_custom(urls)


def main() -> None:
    sources_cfg = load_yaml(CONFIG_DIR / "sources.yaml")
    keywords_cfg = load_yaml(CONFIG_DIR / "keywords.yaml")
    pipelines_cfg = load_yaml(CONFIG_DIR / "pipelines.yaml")

    keywords = (
        keywords_cfg.get("keywords", {}).get("companies", [])
        + keywords_cfg.get("keywords", {}).get("sectors", [])
        + keywords_cfg.get("keywords", {}).get("events", [])
    )

    raw_records = []
    clean_records = []
    report_items = []

    if pipelines_cfg.get("pipelines", {}).get("crawl", True):
        for source in sources_cfg.get("sources", []):
            if not source.get("enabled", True):
                continue
            results = crawl_by_type(source.get("type", "custom"), source.get("urls", []))
            for item in results:
                raw_records.append(
                    {
                        "source": source.get("name", ""),
                        "url": item.url,
                        "status_code": item.status_code,
                        "metadata": item.metadata,
                        "html": item.text,
                    }
                )

                if not pipelines_cfg.get("pipelines", {}).get("parse", True):
                    continue

                parsed = extract_text(item.text)
                clean_record = {
                    "source": source.get("name", ""),
                    "url": item.url,
                    "title": parsed.get("title", ""),
                    "text": parsed.get("text", ""),
                }
                clean_records.append(clean_record)

                signals = {}
                if pipelines_cfg.get("pipelines", {}).get("signals", True):
                    signals = extract_signals(clean_record["text"], keywords)

                summary = ""
                if pipelines_cfg.get("pipelines", {}).get("summarize", True):
                    summary = summarize_text(clean_record["text"]).get("summary", "")

                report_items.append(
                    {
                        "title": clean_record["title"] or clean_record["url"],
                        "summary": summary,
                        "signals": signals,
                    }
                )

    if raw_records:
        write_jsonl(DATA_DIR / "raw" / "raw.jsonl", raw_records)
    if clean_records:
        write_jsonl(DATA_DIR / "clean" / "clean.jsonl", clean_records)
    if report_items and pipelines_cfg.get("pipelines", {}).get("report", True):
        report = build_report(report_items)
        write_text(DATA_DIR / "reports" / "daily_report.md", report)


if __name__ == "__main__":
    main()
