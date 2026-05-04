import requests
import xml.etree.ElementTree as ET
import logging
import time
from app.configuration import settings
from app.utils import clean_html, extract_full_article, score_article, is_noise, parse_item

logging.basicConfig(level=logging.INFO)

def crawl_news(keyword="bitcoin", limit=5):
    articles = []

    for source_url in settings.rss_sources:
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

                    time.sleep(1) 

                except Exception as e:
                    logging.warning(f"Item error: {e}")

        except Exception as e:
            logging.warning(f"Source error: {e}")

    # sort theo score
    articles = sorted(articles, key=lambda x: x["score"], reverse=True)

    return articles[:limit]
