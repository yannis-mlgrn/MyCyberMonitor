import feedparser
from app.models.blogPost import BlogPost
from datetime import datetime
import json

rss_url = {
    "Synactiv": "https://www.synacktiv.com/en/feed/lastblog.xml",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Conquer Your Risk": (
        "https://www.conquer-your-risk.com/category/articles/feed"
    ),
    "Quarkslab": "https://blog.quarkslab.com/feeds/all.atom.xml",
    "Kaspersky": "https://www.kaspersky.com/blog/feed/"
}


def get_rss_feed(rss_url: dict = rss_url, n: int = 5):
    """
    fetch the RSS feed from the given URL and return the parsed feed.
    It fetches the 'n' most recent entries from each feed.
    These entries are returned as a list of BlogPost objects.
    """
    final_feed = []
    with open('app/data/blogpost.json', "r", encoding="utf-8") as data:
        posts = json.load(data)
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
            # Check if the title matches an existing post and get its vote
            existing_post = next(
                (post for post in posts if post["title"] == entry.title),
                None
            )
            vote = existing_post["vote"] if existing_post else 0
            # Check the format of the published date
            if not is_isoformat(entry.published):
                entry.published = datetime.strptime(
                        entry.published, "%a, %d %b %Y %H:%M:%S %z"
                    ).isoformat()
            final_feed.append(
                BlogPost(
                    title=f"[{source_key}] : {entry.title}",
                    link=entry.link,
                    description=entry.description,
                    published=entry.published,
                    author=(
                        entry.author
                        if hasattr(entry, 'author')
                        else source_key
                    ),
                    vote=vote
                )
            )
    # Sort the list of blog posts by published date
    final_feed = sorted(
        final_feed, key=lambda post: post.published, reverse=True
    )
    # Create the output JSON file
    json_object = json.dumps(
        [post.model_dump() for post in final_feed],
        indent=4
    )
    # Write the JSON object to a file
    with open('app/data/blogpost.json', "w") as outfile:
        outfile.write(json_object)


def is_isoformat(date_str: str) -> bool:
    """
    Check if the given date string is in ISO format.
    """
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False
