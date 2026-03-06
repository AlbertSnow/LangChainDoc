from typing import Dict, List


def extract_signals(text: str, keywords: List[str]) -> Dict[str, List[str]]:
    matched = [kw for kw in keywords if kw and kw in text]
    return {"matched_keywords": matched}
