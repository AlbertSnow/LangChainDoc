from typing import Dict, List


def build_report(items: List[Dict[str, str]]) -> str:
    lines = ["# 投资信息日报", ""]
    for item in items:
        title = item.get("title", "无标题")
        summary = item.get("summary", "")
        lines.append(f"## {title}")
        lines.append(summary)
        lines.append("")
    return "\n".join(lines)
