from src.crawler import Crawler
from src.log_config import get_logger

logger = get_logger("NOTIFIER")

def notify(crawler: Crawler):
    try:
        if crawler.products_scraped:
            logger.debug(f"Total No of products scraped -> {crawler.products_scraped}")
    except Exception as e:
        logger.warning(f"Exception occurred in notification service {e}")
    