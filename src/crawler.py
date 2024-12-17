import os
import requests
from time import sleep
from typing import Optional
from bs4 import BeautifulSoup
from src.abstracts.AbstractCrawler import AbstractCrawler
from src.models.product import Product
from src.utils import get_random_user_agent
from src.constants import *
from src.log_config import get_logger
from src.db import get_redis_conn

logger = get_logger("CRAWLER")
redis_conn = get_redis_conn()

class Crawler(AbstractCrawler):
    def __init__(self, page_limit: int = None, proxy: Optional[str]= None):
        super().__init__(page_limit, proxy)
        self.session = requests.session() 
        self.products_scraped: int = 0

    def crawl(self):
        """
            Method to crawl pages of the website one after another.
            Maintain state of the current page crawled
        """
        current_page = 1
        logger.info(f"Initialising Crawling with page_limit : {self.page_limit}")
        try:
            while current_page <= self.page_limit:
                # We do not want to show more products than the user wants to see
                url = f"https://dentalstall.com/shop/page/{current_page}"
                logger.info(f"Hitting page:{current_page}, {url}")
                status, response = self.process_request(url)
                if status == OK and isinstance(response, requests.Response):
                    self.parse_response(response)
                    current_page += 1
                else:
                    logger.warning(f"Failed to fetch page {current_page}")
                    break
        except Exception as e:
            logger.warning(f"Exception {e} occurred while crawling page {current_page}")

    def is_product_price_updated(self, product_title: str, product_price: float):
        try:
            price_cached = redis_conn.get(product_title)
            if price_cached and float(product_price) == float(price_cached):
                logger.debug(f"Price is same no need to update product -> {product_title}")
                return False
            logger.info(f"Price changed, caching new price {product_title}, {product_price}")
            redis_conn.set(product_title, float(product_price), ex=60)
            return True
        except Exception as e:
            logger.warning(f"Exception occurred while checking cache {product_title}, {e}")
        return False

    def parse_response(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_block = soup.find("ul",attrs={"class": "products"})
            product_list = product_block.find_all("li")
            for ind in range(len(product_list)):
                try:
                    product = product_list[ind]
                    thumbnail = product.find("div", attrs={"class": "mf-product-thumbnail"})
                    price_box = product.find("div", attrs={"class": "mf-product-price-box"})
                    product_title = product.find("h2", attrs={"class": "woo-loop-product__title"}).text
                    product_price = price_box.find("bdi").text.split("₹")[-1]
                    img_tag = thumbnail.find("img")
                    if img_tag:
                        product_title = img_tag["title"].replace("- Dentalstall India", "").strip()
                        img_url = img_tag["data-lazy-srcset"].split(",")[0].split(" ")[0].strip()
                        img_src = self.save_image(image_url=img_url, product_title=product_title)
                    else:
                        img_src=IMAGE_SRC_NOT_FOUND
                    if product_title and product_price and img_src != IMAGE_SRC_NOT_FOUND:
                        self.products_scraped += 1
                        if not self.is_product_price_updated(product_title, product_price):
                            self.products.append(Product(
                                product_price=product_price, product_title=product_title, path_to_image=img_src
                            ))
                except Exception as e:
                    logger.warning(f"Exception {e} occurred for product index {ind}")
                    continue
            logger.info(f"Page Complete, data generated for -> {self.products_scraped} products" )
        except Exception as e:
            logger.warning(f"Exception {e} occurred while parsing")
        
    def process_request(self, url):
        """
            @GET Request to the endpoint "https://dentalstall.com/shop/page/{page_no}"
            params: URL
        """
        retries = 3 
        timeout = 1
        request_headers = { "User-Agent": get_random_user_agent() }
        proxies = None
        if self.proxy_uri:
            proxies = {"https": self.proxy_uri, "http": self.proxy_uri}
        for trial in range(retries):
            timeout = timeout+retries
            try:
                response = self.session.get(url=url, headers=request_headers, proxies=proxies, timeout=timeout)
                logger.info(f"status_code for url {url} -> {response.status_code}, latency -> {response.elapsed.total_seconds()}")
                if response.status_code == 200:
                    return [OK, response]
            except Exception as e:
                logger.warning(f"Exception {e} occurred while processing url->{url}, in trial {trial}. retrying in 2 seconds...")
            sleep(2)                
        return [FAILURE, None]

    def save_image(self, image_url: str, product_title: str):
        """
            Need to save the product's image (jpg)
            return the file path where photo is saved
        """
        try:
            resp = self.session.get(url=image_url)
            directory = "images"
            product_title = product_title.replace("/", " ")
            file_path = f"images/{product_title}.jpg"
            if not os.path.exists(directory):
                os.makedirs(directory)
                file_path = os.path.join(directory, product_title+".jpg")
            with open(file=file_path, mode='wb') as f:
                f.write(resp.content)
            return file_path
        except Exception as e:
            logger.warning(f"Exception occurred while saving photo of {product_title}", e)
        return IMAGE_SRC_NOT_FOUND            


if __name__ == "__main__":
    limit = int(input())
    crawler = Crawler(limit)
    crawler.crawl()
    print(f"Total Products Scraped {crawler.products_scraped}")
