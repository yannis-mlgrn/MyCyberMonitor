from fastapi import FastAPI
from typing import List
from app.utils.cveScraping import get_cve_list
from app.utils.RSSfeedscraping import get_rss_feed
from app.models.cve import CVE
from app.models.blogPost import BlogPost
import json
from pathlib import Path


app = FastAPI(
    title="My Cyber Monitor",
    version="0.1",
    description="Cyber threat intelligence monitor API (CVE, blogs, etc.)"
)

# initialize the data
get_rss_feed()
get_cve_list()


@app.get("/cve/recent", response_model=List[CVE], tags=["CVE"])
async def get_recent_cves(n: int = 5) -> List[CVE]:
    """
    Get the most recent 'n' CVEs by scraping data from the Vulmon website.
    Defaults to 5 if 'n' is not provided.
    """
    cve_json_file_path = (
        Path(__file__).resolve().parent.parent / "app" / "data" / "cve.json"
    )
    return json.loads(cve_json_file_path.read_text(encoding="utf-8"))[:n]


@app.get("/blogs/latest", response_model=List[BlogPost], tags=["Blogs"])
async def get_latest_blog_articles():
    """
    Get latest blog posts from selected cyber security blogs
    (RSS parsing mock).
    """
    data_file = "blogpost.json"
    blogPost_json_file_path = (
        Path(__file__).resolve().parent.parent / "app" / "data" / data_file
    )
    return json.loads(blogPost_json_file_path.read_text(encoding="utf-8"))
