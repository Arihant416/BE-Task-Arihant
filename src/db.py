import json
import redis
from typing import List
from src.models.product import Product
from src.log_config import get_logger
from fastapi.encoders import jsonable_encoder

redis_conn = None

logger = get_logger("DB")

# Could be a sqlite db or other sql or nosql db
def update_db(file_name: str, products:List[Product]):
    if products:
        with open(file=file_name, mode='w') as f:
            # We are basically dumping all products in a json file for now. That json file is our db.
            json.dump(jsonable_encoder(products), f, indent=2)
        logger.info(f"{len(products)} items saved")
    else:
        logger.info("No Products to Save")
    


def get_redis_conn():
    global redis_conn
    try:
        if redis_conn is None:
            logger.info("Creating new redis connection")
            redis_conn = redis.Redis(host="localhost", port=6379, decode_responses=True)
        else:
            logger.info("Using exising redis connection")
        return redis_conn
    except Exception as e:
        logger.error(f"Exception in connecting with Redis {e}")
    
if __name__ == "__main__":
    conn = get_redis_conn()
    print(conn.get("name"))