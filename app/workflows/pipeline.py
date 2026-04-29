from app.tools.crawl import crawl_news
from app.core.llm import call_llm
from app.tools.article_extractor import extract_article
import logging
from app.core.promt import summary_prompt

logging.basicConfig(level=logging.INFO)

def run_pipeline(keyword):
    logging.info(f"Start pipeline with keyword: {keyword}")

    news_list = crawl_news(keyword)
    
    results = []

    for i, item in enumerate(news_list):
        print(f"Processing: {item['title']}")

        article = extract_article(item["link"])

        if "error" in article or not article.get("text"):
            logging.warning(f"Failed to extract article: {item['link']} - {article.get('error', 'No text found')}")
            continue

        prompt = summary_prompt(article["text"][:5000])
        summary = call_llm(prompt)
        logging.info(f"Summary generated for {keyword}: {summary}")
        results.append({
            "title": article["title"],
            "summary": summary,
            "url": item["link"]
        })

    return results