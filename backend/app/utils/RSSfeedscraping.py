import feedparser
from app.models.blogPost import BlogPost
from datetime import datetime

rss_url = {
    "synactiv": "https://www.synacktiv.com/en/feed/lastblog.xml",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "conquer-your-risk": (
        "https://www.conquer-your-risk.com/category/articles/feed"
    )
}


def get_rss_feed(rss_url: dict = rss_url, n: int = 5) -> list[BlogPost]:
    """
    fetch the RSS feed from the given URL and return the parsed feed.
    It fetches the 'n' most recent entries from each feed.
    These entries are returned as a list of BlogPost objects.
    """
    final_feed = []
    for url in rss_url.values():
        # Parse le flux RSS
        feed = feedparser.parse(url)
        for entry in feed.entries[:n]:
            source_key = next(
                (key for key, value in rss_url.items() if value == url),
                "unknown"
            )
            if (
                hasattr(entry, 'author') and
                ('@' in entry.author or 'webmaster' in entry.author.lower())
            ):
                entry.author = source_key
            # Create the output list
            final_feed.append(
                BlogPost(
                    title=entry.title,
                    link=entry.link,
                    description=entry.description,
                    published=datetime.strptime(
                        entry.published, "%a, %d %b %Y %H:%M:%S %z"
                    ),
                    author=(
                        entry.author
                        if hasattr(entry, 'author')
                        else source_key
                    ),
                    vote=0
                )
            )
    # Return the sorted list of blog posts by published date
    return sorted(final_feed, key=lambda post: post.published, reverse=True)
