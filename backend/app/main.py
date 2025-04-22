from fastapi import FastAPI
from typing import List
from app.utils.cveScraping import get_cve_list
from app.utils.RSSfeedscraping import get_rss_feed
from app.models.cve import CVE
from app.models.blogPost import BlogPost


app = FastAPI(
    title="My Cyber Monitor",
    version="0.1",
    description="Cyber threat intelligence monitor API (CVE, blogs, etc.)"
)


@app.get("/cve/recent", response_model=List[CVE], tags=["CVE"])
async def get_recent_cves(n: int = 5) -> List[CVE]:
    """
    Get the most recent 'n' CVEs by scraping data from the Vulmon website.
    Defaults to 5 if 'n' is not provided.
    """
    return get_cve_list(n)


@app.get("/blogs/latest", response_model=List[BlogPost], tags=["Blogs"])
async def get_latest_blog_articles():
    """
    Get latest blog posts from selected cyber security blogs
    (RSS parsing mock).
    """
    return get_rss_feed()
