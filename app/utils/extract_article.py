from newspaper import Article
import logging

logging.basicConfig(level=logging.INFO)


def extract_article(url: str):
    """Extract article content from URL using newspaper3k"""
    try:
        logging.info(f"Extracting article from: {url}")
        
        article = Article(url)
        article.download()
        
        if not article.html:
            logging.warning(f"No HTML content downloaded for {url}")
            return {"error": "No HTML content downloaded"}
        
        article.parse()
        
        if not article.text:
            logging.warning(f"No text found in article: {url}")
            return {"error": "No text found"}
        
        logging.info(f"Successfully extracted: {article.title} ({len(article.text)} chars)")
        
        return {
            "title": article.title,
            "text": article.text
        }

    except Exception as e:
        logging.warning(f"Newspaper failed: {url} - {e}")