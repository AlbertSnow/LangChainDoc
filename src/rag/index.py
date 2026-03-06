from typing import List, Dict


def build_index(docs: List[Dict[str, str]]) -> Dict[str, int]:
    return {"documents": len(docs)}
