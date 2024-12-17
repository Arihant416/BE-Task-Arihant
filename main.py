from typing import Optional
from crawler import Crawler
from notifier import notify
from log_config import get_logger
from fastapi import FastAPI, Depends, HTTPException, Header
from starlette.responses import JSONResponse

app = FastAPI()
logger = get_logger("MAIN")

AUTH_TOKEN = "AtlYs-SenIoR/SofTWaReEnGinEer-BE3+"

def is_token_valid(token: str = Header(...)):
    if token != AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidded | token invalid")
    

@app.post('/crawl', dependencies=[Depends(is_token_valid)])
def scrape_products(page_limit: Optional[int] = None, proxy_uri: Optional[str] = None):
    logger.info("Starting Crawling Automation")
    try:
        crawler = Crawler(page_limit=page_limit, proxy=proxy_uri)
        crawler.crawl()
        crawler.update_db("data.json")
        notify(crawler)
        return JSONResponse(content={"data": crawler.products, "message": f"Scraped {crawler.products_scraped} products"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": f"Some exception {e} occurred"}, status_code=503)
    