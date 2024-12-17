import json
from src.crawler import Crawler
from src.log_config import get_logger

logger = get_logger("DB")

# Could be a sqlite db or other sql or nosql db
def update_db(file_name: str, crawler: Crawler):
    with open(file=file_name, mode='w') as f:
        # We are basically dumping all products in a json file for now. That json file is our db.
        json.dump([product.dict() for product in crawler.products], f, indent=2)
    logger.info(f"{crawler.products_scraped} items saved")