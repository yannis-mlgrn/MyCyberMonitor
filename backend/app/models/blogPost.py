from pydantic import BaseModel


class BlogPost(BaseModel):
    title: str
    description: str
    link: str
    published: str
    author: str
    vote: int = 0
