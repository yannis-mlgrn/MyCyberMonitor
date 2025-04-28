import feedparser
from app.models.blogPost import BlogPost
from datetime import datetime
import json
from dateutil import parser

rss_url = {
    "Synactiv": "https://www.synacktiv.com/en/feed/lastblog.xml",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Conquer Your Risk": (
        "https://www.conquer-your-risk.com/category/articles/feed"
    ),
    "Quarkslab": "https://blog.quarkslab.com/feeds/all.atom.xml",
    "Kaspersky": "https://www.kaspersky.com/blog/feed/",
    "Intigriti": "https://www.intigriti.com/blog/feed",
    "Infosec Writeups": "https://infosecwriteups.com/feed",
    "hackerone": "https://www.hackerone.com/taxonomy/term/291/feed",
    "Root-Me": "https://blog.root-me.org/index.xml",
    "HACKADAY": "https://hackaday.com/feed/",
}


def get_rss_feed(rss_url: dict = rss_url, n: int = 15):
    """
    fetch the RSS feed from the given URL and return the parsed feed.
    It fetches the 'n' most recent entries from each feed.
    These entries are returned as a list of BlogPost objects.
    """
    final_feed = []
    with open('app/data/blogpost.json', "r", encoding="utf-8") as data:
        posts = json.load(data)
    for url in rss_url.values():
        # Parse the RSS feed
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
            entry.published = parse_rss_date(entry.published)
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


def parse_rss_date(date_str: str) -> str:
    """
    Parse the RSS date and return an ISO formatted string.
    It handles both ISO format and other date formats, including
    'Sun, 27 Apr 2025 00:00:00 GMT'.
    """
    try:
        # First, try to parse ISO format
        return datetime.fromisoformat(date_str).isoformat()
    except ValueError:
        try:
            # If it fails, attempt to use dateutil.parser.parse
            # for other formats
            parsed_date = parser.parse(date_str)
            return parsed_date.isoformat()
        except (ValueError, TypeError) as e:
            print(f"Error parsing date: {date_str} - {e}")
            return date_str  # Return the original date string if parsing fails
