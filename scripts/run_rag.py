from pathlib import Path
import json

from src.rag.index import build_index


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def main() -> None:
    clean_path = DATA_DIR / "clean" / "clean.jsonl"
    if not clean_path.exists():
        raise SystemExit("clean.jsonl not found. Run scripts/run_pipeline.py first.")

    docs = []
    with clean_path.open("r", encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line))

    index_info = build_index(docs)
    print(index_info)


if __name__ == "__main__":
    main()
