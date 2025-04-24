from fastapi import FastAPI, HTTPException
from typing import List
from app.utils.cveScraping import get_cve_list
from app.utils.RSSfeedscraping import get_rss_feed
from app.models.cve import CVE
from app.models.blogPost import BlogPost
from app.models.voteRequest import VoteRequest
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="My Cyber Monitor",
    version="0.1",
    description="Cyber threat intelligence monitor API (CVE, blogs, etc.)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # toutes les origines
    allow_credentials=True,
    allow_methods=["*"],            # toutes les méthodes GET, POST, etc.
    allow_headers=["*"],            # tous les headers
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


@app.post("/blogs/vote", response_model=List[BlogPost], tags=["Voting"])
async def vote(req: VoteRequest):
    """
    Cast a vote for a given article title.
    """
    title = req.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title must not be empty")
    with open('app/data/blogpost.json', "r", encoding="utf-8") as data:
        posts = json.load(data)
    found = False
    for post in posts:
        if post.get("title") == title:
            post["vote"] += 1
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="Title not found")
    with open("app/data/blogpost.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    return posts


@app.post("/blogs/unvote", response_model=List[BlogPost], tags=["Voting"])
async def unvote(req: VoteRequest):
    """
    Cast a vote for a given article title.
    """
    title = req.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title must not be empty")
    with open('app/data/blogpost.json', "r", encoding="utf-8") as data:
        posts = json.load(data)
    found = False
    for post in posts:
        if post.get("title") == title:
            post["vote"] -= 1
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="Title not found")
    with open("app/data/blogpost.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    return posts
