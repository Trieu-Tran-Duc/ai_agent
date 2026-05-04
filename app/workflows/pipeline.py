import logging
from app.tools.crawl_tool import crawl_news
from app.utils import extract_article
from app.configuration import setup_logging

logger = logging.getLogger("pipeline")


def run_pipeline(keyword):
    setup_logging(logging.INFO)
    logger.info(f"Start pipeline with keyword: {keyword}")

    # step 1: crawl news
    news_list = crawl_news(keyword)

    # step 2: extract article + summarize with LLM
    articles = []
    for i, item in enumerate(news_list):
        print(f"Processing: {item['title']}")

        article = extract_article(item["link"])

        if "error" in article or not article.get("text"):
            logging.warning(f"Skip: {item['link']}")
            continue

        articles.append(
            {
                "title": article["title"],
                "content": article["text"][:2000],
                "url": item["link"],
            }
        )

        articles = articles[:10]
        if not articles:
            logging.error("No valid articles")
            return {"keyword": keyword, "articles": [], "error": "No valid articles collected"}

        logging.info(f"Collected {len(articles)} articles")

        # results = Agent.run({"articles": articles})
        return {"keyword": keyword, "articles": articles}
