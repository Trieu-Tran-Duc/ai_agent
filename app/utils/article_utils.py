import logging
from newspaper import Article
from bs4 import BeautifulSoup


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def extract_full_article(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logging.warning(f"Newspaper failed: {url} - {e}")
        return ""