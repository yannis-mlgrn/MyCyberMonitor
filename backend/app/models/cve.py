from pydantic import BaseModel
from typing import Optional


class CVE(BaseModel):
    id: str
    cvss: Optional[float] = None
    description: str
    link: str
