from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from app.utils.cveScraping import get_cve_list
from app.models.cve import CVE

app = FastAPI(
    title="My Cyber Monitor",
    version="0.1",
    description="Cyber threat intelligence monitor API (CVE, blogs, etc.)"
)


class BlogPost(BaseModel):
    title: str
    resume: str
    reference: str
    published: str
    tags: List[str] = []


@app.get("/cve/recent", response_model=List[CVE], tags=["CVE"])
async def get_recent_cves(n: int = 5) -> List[CVE]:
    """
    Get the most recent 'n' CVEs from CIRCL public API.
    Defaults to 5 if 'n' is not provided.
    """
    return get_cve_list(n)


@app.get("/blogs/latest", response_model=List[BlogPost], tags=["Blogs"])
async def get_latest_blog_articles():
    """
    Get latest blog posts from selected cyber security blogs
    (RSS parsing mock).
    """
    # TODO : Implement RSS feed parsing
    return [
        BlogPost(
            title="Supply Chain Attack Hits NPM",
            resume=(
                "A new supply chain attack has been discovered "
                " in the NPM ecosystem, affecting thousands of packages."
            ),
            reference="https://thehackernews.com/2025/04/npm-attack.html",
            published="2025-04-21",
            tags=["supply chain", "npm", "attack"]
        ),
        BlogPost(
            title="Zero-Day in Cisco Routers",
            resume=(
                "A zero-day vulnerability has been found in Cisco routers, "
                "allowing remote code execution."
            ),
            reference="https://threatpost.com/zero-day-cisco/187654/",
            published="2025-04-20",
            tags=["Cisco", "zero-day", "vulnerability"]
        )
    ]
