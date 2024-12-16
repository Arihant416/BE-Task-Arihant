import requests
import json
from bs4 import BeautifulSoup
from typing import Optional

class Crawler:
    def __init__(self, page_limit: Optional[int] = None, proxy: Optional[str]= None):
        self.page_limit = page_limit
        self.proxy = proxy

        

