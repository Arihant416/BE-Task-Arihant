from typing import Optional
from src.crawler import Crawler
from src.notifier import notify
from src.log_config import get_logger
from src.models.request import Request
from src.db import update_db
from src.constants import *
from fastapi import FastAPI, Depends, HTTPException, Header
from starlette.responses import JSONResponse

app = FastAPI()
logger = get_logger("MAIN")

AUTH_TOKEN = "AtlYs-SenIoR/SofTWaReEnGinEer-BE3+"

def is_token_valid(token: str = Header(...)):
    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Forbidded | token invalid")
    

@app.post('/crawl', dependencies=[Depends(is_token_valid)])
def scrape_products(request: Request):
    logger.info("Starting Crawling Automation")
    try:
        crawler = Crawler(page_limit=request.page_limit, proxy=request.proxy)
        crawler.crawl()
        update_db(file_name="data.json", crawler=crawler)
        notify(crawler)
        return JSONResponse(content={"message": f"Scraped {crawler.products_scraped} products", "status": OK}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": f"Some exception {e} occurred", "status": FAILURE}, status_code=503)
    