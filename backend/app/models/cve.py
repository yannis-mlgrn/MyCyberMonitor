from pydantic import BaseModel


class CVE(BaseModel):
    id: str
    description: str
    link: str
