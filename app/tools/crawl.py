import requests
import xml.etree.ElementTree as ET
import logging
import time
from newspaper import Article
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

# ====== CONFIG ======
RSS_SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss.xml",
    "https://decrypt.co/feed",
    "https://feeds.bloomberg.com/crypto/news.rss"
]

ANALYSIS_KEYWORDS = [
    "analysis", "analyst", "opinion", "insight",
    "forecast", "prediction", "outlook",
    "market analysis", "market wrap", "trend",
    "bullish", "bearish", "price target",
    "technical analysis", "on-chain", "sentiment",
    "deep dive", "review"
]

NOISE_KEYWORDS = [
    "breaking", "just in", "announced",
    "files for", "launches", "partners with"
]

# ====== HELPERS ======

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def extract_full_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logging.warning(f"Newspaper failed: {url} - {e}")
        return ""


def parse_item(item):
    def get(tag):
        el = item.find(tag)
        return el.text.strip() if el is not None and el.text else ""

    title = get("title")
    link = get("link")

    content = (
        get("description") or
        get("{http://purl.org/rss/1.0/modules/content/}encoded")
    )

    return title, link, content


def is_noise(title):
    text = title.lower()
    return any(k in text for k in NOISE_KEYWORDS)


def score_article(title, content):
    text = (title + " " + content).lower()
    score = 0

    for kw in ANALYSIS_KEYWORDS:
        if kw in text:
            score += 2

    # bonus chuyên sâu
    if "on-chain" in text:
        score += 3
    if "technical analysis" in text:
        score += 3
    if "price prediction" in text:
        score += 3

    return score


# ====== MAIN ======

def crawl_news(keyword="bitcoin", limit=5):
    articles = []

    for source_url in RSS_SOURCES:
        try:
            logging.info(f"Fetching: {source_url}")
            res = requests.get(source_url, timeout=10)

            if res.status_code != 200:
                continue

            root = ET.fromstring(res.content)
            items = root.findall(".//item")[:10]

            for item in items:
                try:
                    title, link, content = parse_item(item)

                    if not title or not link:
                        continue

                    if is_noise(title):
                        continue

                    text_check = (title + " " + content).lower()

                    # filter keyword bitcoin
                    # if keyword.lower() not in text_check and "btc" not in text_check:
                    #     continue

                    # crawl full article
                    full_text = extract_full_article(link)

                    final_content = full_text if full_text else clean_html(content)

                    if not final_content:
                        continue

                    score = score_article(title, final_content)

                    if score >= 3:
                        articles.append({
                            "title": title,
                            "link": link,
                            "content": final_content,
                            "score": score
                        })

                        logging.info(f"Added ({score}): {title}")

                    time.sleep(1)  # tránh bị block

                except Exception as e:
                    logging.warning(f"Item error: {e}")

        except Exception as e:
            logging.warning(f"Source error: {e}")

    # sort theo score
    articles = sorted(articles, key=lambda x: x["score"], reverse=True)

    return articles[:limit]
