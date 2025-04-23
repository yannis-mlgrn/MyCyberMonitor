from pydantic import BaseModel


class VoteRequest(BaseModel):
    title: str
