from typing import Dict


def summarize_text(text: str, max_chars: int = 600) -> Dict[str, str]:
    summary = text[:max_chars].strip()
    return {"summary": summary}
