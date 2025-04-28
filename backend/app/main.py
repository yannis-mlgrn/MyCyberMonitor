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
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="My Cyber Monitor",
    version="0.1",
    description="Cyber threat intelligence monitor API (CVE, blogs, etc.)"
)

scheduler = BackgroundScheduler()


def scrapping_data():
    logger.info("Starting scheduled scraping tasks.")
    get_rss_feed()
    logger.info("RSS feed scraping completed successfully.")
    get_cve_list()


# Data initialization
scrapping_data()

# Schedule the scraping task to run every 2 hours
scheduler.add_job(scrapping_data, 'interval', hours=2)
scheduler.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mycybermonitor.yannis-mlgrn.fr",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/cve/recent", response_model=List[CVE], tags=["CVE"])
async def get_recent_cves(n: int = 5) -> List[CVE]:
    """
    Get the most recent 'n' CVEs by scraping data from the Vulmon website.
    Defaults to 5 if 'n' is not provided.
    """
    logger.info(f"Fetching the {n} most recent CVEs.")
    cve_json_file_path = (
        Path(__file__).resolve().parent.parent / "app" / "data" / "cve.json"
    )
    try:
        cves = json.loads(cve_json_file_path.read_text(encoding="utf-8"))[:n]
        logger.info(f"Successfully fetched {len(cves)} CVEs.")
        return cves
    except Exception as e:
        logger.error(
            f"Error fetching CVEs: {e}"
        )
        raise HTTPException(status_code=500, detail="Error fetching CVEs")


@app.get("/blogs/latest", response_model=List[BlogPost], tags=["Blogs"])
async def get_latest_blog_articles():
    """
    Get latest blog posts from selected cyber security blogs
    (RSS parsing mock).
    """
    logger.info("Fetching the latest blog articles.")
    data_file = "blogpost.json"
    blogPost_json_file_path = (
        Path(__file__).resolve().parent.parent / "app" / "data" / data_file
    )
    try:
        blog_posts = json.loads(
            blogPost_json_file_path.read_text(encoding="utf-8")
        )
        logger.info(f"Successfully fetched {len(blog_posts)} blog articles.")
        return blog_posts
    except Exception as e:
        logger.error(f"Error fetching blog articles: {e}")
        raise HTTPException(
            status_code=500,
            detail=(
                "Error fetching blog articles"
            )
        )


@app.post("/blogs/vote", response_model=List[BlogPost], tags=["Voting"])
async def vote(req: VoteRequest):
    """
    Cast a vote for a given article title.
    """
    title = req.title.strip()
    logger.info(f"Voting for blog post with title: {title}")
    if not title:
        logger.warning("Vote request failed: Title is empty.")
        raise HTTPException(status_code=400, detail="Title must not be empty")
    try:
        with open('app/data/blogpost.json', "r", encoding="utf-8") as data:
            posts = json.load(data)
        found = False
        for post in posts:
            if post.get("title") == title:
                post["vote"] += 1
                found = True
                logger.info(f"Vote cast for blog post: {title}")
        if not found:
            logger.warning(f"Vote request failed: Title '{title}' not found.")
            raise HTTPException(status_code=404, detail="Title not found")
        with open("app/data/blogpost.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        return posts
    except Exception as e:
        logger.error(f"Error processing vote request: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error processing vote request"
        )


@app.post("/blogs/unvote", response_model=List[BlogPost], tags=["Voting"])
async def unvote(req: VoteRequest):
    """
    Remove a vote for a given article title.
    """
    title = req.title.strip()
    logger.info(f"Unvoting for blog post with title: {title}")
    if not title:
        logger.warning("Unvote request failed: Title is empty.")
        raise HTTPException(status_code=400, detail="Title must not be empty")
    try:
        with open('app/data/blogpost.json', "r", encoding="utf-8") as data:
            posts = json.load(data)
        found = False
        for post in posts:
            if post.get("title") == title:
                post["vote"] -= 1
                found = True
                logger.info(f"Vote removed for blog post: {title}")
        if not found:
            logger.warning(
                f"Unvote request failed: Title '{title}' not found."
            )
            raise HTTPException(status_code=404, detail="Title not found")
        with open("app/data/blogpost.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        return posts
    except Exception as e:
        logger.error(f"Error processing unvote request: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error processing unvote request"
        )
