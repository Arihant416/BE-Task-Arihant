from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel


class AbstractCrawler(ABC):
    def __init__(self, page_limit: int = None, proxy: Optional[str] = None):
        self.proxy_uri = proxy
        self.page_limit = page_limit
        self.products = []
        
    @abstractmethod
    def crawl(self):
        raise NotImplementedError


    @abstractmethod
    def process_request(self, url: str):
        raise NotImplementedError

    @abstractmethod
    def save_image(self,  image_url: str, product_title: str):
        raise NotImplementedError