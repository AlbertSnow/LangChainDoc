from typing import Dict

from bs4 import BeautifulSoup


def extract_text(html: str) -> Dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()
    text = " ".join(soup.get_text(separator=" ", strip=True).split())
    return {"title": title, "text": text}
