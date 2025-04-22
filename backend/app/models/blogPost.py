from datetime import datetime
from pydantic import BaseModel


class BlogPost(BaseModel):
    title: str
    description: str
    link: str
    published: datetime
    author: str
    vote: int = 0
