import json
import requests
import os
from bs4 import BeautifulSoup
from typing import Optional

from utils import get_random_user_agent
from constants import *

class Crawler:
    def __init__(self, page_limit: Optional[int] = None, proxy: Optional[str]= None):
        self.page_limit = page_limit
        self.proxy_uri = proxy
        self.products = []
        self.session = requests.session() 
        self.product_scraped: int = 0

    def crawl(self):
        """
            Method to crawl pages of the website one after another.
            Maintain state of the current page crawled
        """
        current_page = 1
        try:
            while True:
                # We do not want to show more products than the user wants to see
                if self.page_limit and current_page > self.page_limit:
                    break
                
                url = f"https://dentalstall.com/shop/page/{current_page}"
                status, response = self.process_request(url)
                if status == OK and isinstance(response, requests.Response):
                    self.parse_response(response)
                    current_page += 1
                else:
                    break
        except Exception as e:
            print(f"Exception {e} occurred while crawling page {current_page}")


    def parse_response(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_block = soup.find("ul",attrs={"class": "products"})
            product_list = product_block.find_all("li")
            for product in product_list:
                price = product.find("span", attrs={"class": "price"}).find("bdi").text
                image = product.find("img")
                if image and image.has_attr("title"):
                    title = image["title"].replace("- Dentalstall India", "").strip()
                else:
                    title = product.find("h2").text
                if image and image.has_attr("data-lazy-srcset"):
                    img_url = image["data-lazy-srcset"].split(",")[0].split(" ")[0].strip()
                    img_src = self.save_image(img_url, title)
                else:
                    img_src = IMAGE_SRC_NOT_FOUND
                print(title, price, img_src)
                if title and price and img_src != IMAGE_SRC_NOT_FOUND:
                    self.product_scraped += 1
            print("Count -> ", self.product_scraped)
        except Exception as e:
            print(f"Exception {e} occurred while parsing")
        
    def process_request(self, url):
        """
            @GET Request to the endpoint "https://dentalstall.com/shop/page/{page_no}"
            Params: URL
        """
        request_headers= { "User-Agent": get_random_user_agent() }
        proxies = None
        if self.proxy_uri:
            proxies = {"https": self.proxy_uri, "http": self.proxy_uri}
        try:
            response = self.session.get(url=url, headers=request_headers, proxies=proxies)
            print(f"status_code for url {url} -> {response.status_code}, latency -> {response.elapsed.total_seconds()}")
            if response.status_code == 200:
                return [OK, response]
            else:
                return [FAILURE, None]
        except Exception as e:
            print(f"Exception {e} occurred while processing url->{url}")
        return [FAILURE, None]

    def save_image(self, image_url, product_title):
        """
            Need to save the product's image (jpg)
            return the file path where photo is saved
        """
        try:
            resp = self.session.get(url=image_url)
            directory = "images"
            file_path = f"images/{product_title}.jpg"
            if not os.path.exists(directory):
                os.makedirs(directory)
                file_path = os.path.join(directory, product_title+".jpg")
            with open(file=file_path, mode='wb') as f:
                f.write(resp.content)
            return file_path
        except Exception as e:
            print(f"Exception occurred while saving photo of {product_title}", e)
        return IMAGE_SRC_NOT_FOUND

    
            


if __name__ == "__main__":
    limit = int(input())
    crawler = Crawler(limit)
    crawler.crawl()
