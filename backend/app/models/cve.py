from pydantic import BaseModel
from typing import Optional


class CVE(BaseModel):
    id: str
    cvss: Optional[float] = str
    description: str
    link: str
