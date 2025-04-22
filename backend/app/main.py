from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI(
    title="My Cyber Monitor",
    version="0.1",
    description="Cyber threat intelligence monitor API (CVE, blogs, etc.)"
)


# Pydantic Models
class CVE(BaseModel):
    id: str
    title: str
    cvss: float
    published_date: str
    summary: str


class BlogPost(BaseModel):
    title: str
    resume: str
    reference: str
    published: str
    tags: List[str] = []


@app.get("/cve/recent", response_model=List[CVE], tags=["CVE"])
async def get_recent_cves():
    """
    Get the most recent CVEs from CIRCL public API.
    """
    return [
        CVE(
            id="CVE-2025-1234",
            title="Remote Code Execution in Apache Struts",
            cvss=9.8,
            published_date="2025-04-15",
            summary="A remote code execution vulnerability exists in Apache Struts, allowing attackers to execute arbitrary code on the server."
        )
    ]


@app.get("/blogs/latest", response_model=List[BlogPost], tags=["Blogs"])
async def get_latest_blog_articles():
    """
    Get latest blog posts from selected cyber security blogs (RSS parsing mock).
    """
    # Stubbed response (normally you'd parse RSS feeds here)
    return [
        BlogPost(
            title="Supply Chain Attack Hits NPM",
            resume="A new supply chain attack has been discovered in the NPM ecosystem, affecting thousands of packages.",
            reference="https://thehackernews.com/2025/04/npm-attack.html",
            published="2025-04-21",
            tags=["supply chain", "npm", "attack"]
        ),
        BlogPost(
            title="Zero-Day in Cisco Routers",
            resume="A zero-day vulnerability has been found in Cisco routers, allowing remote code execution.",
            reference="https://threatpost.com/zero-day-cisco/187654/",
            published="2025-04-20",
            tags=["Cisco", "zero-day", "vulnerability"]
        )
    ]