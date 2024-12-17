from pydantic import BaseModel
from typing import Optional

class Request(BaseModel):
    page_limit: int
    proxy: Optional[str] = None
