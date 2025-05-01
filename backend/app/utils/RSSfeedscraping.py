import feedparser
from app.models.blogPost import BlogPost
from datetime import datetime, timedelta, timezone
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


def get_rss_feed(rss_url: dict = rss_url):
    """
    Fetch the RSS feed from the given URLs and return the parsed feed.
    It returns only the entries from the last 7 days as BlogPost objects.
    """
    final_feed = []
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    with open('app/data/blogpost.json', "r", encoding="utf-8") as data:
        posts = json.load(data)

    for url in rss_url.values():
        # Parse the RSS feed
        feed = feedparser.parse(url)
        for entry in feed.entries:
            source_key = next(
                (key for key, value in rss_url.items() if value == url),
                "unknown"
            )

            # Try to parse date
            published_str = parse_rss_date(entry.published)
            try:
                published_date = datetime.fromisoformat(published_str)
            except ValueError:
                continue  # Skip if date can't be parsed

            # Filter to keep only posts from the last 7 days
            if published_date < one_week_ago:
                continue

            # Author fallback
            if (
                hasattr(entry, 'author') and
                ('@' in entry.author or 'webmaster' in entry.author.lower())
            ):
                entry.author = source_key

            # Check for existing vote
            existing_post = next(
                (post for post in posts if post["title"] == entry.title),
                None
            )
            vote = existing_post["vote"] if existing_post else 0

            final_feed.append(
                BlogPost(
                    title=f"[{source_key}] : {entry.title}",
                    link=entry.link,
                    description=entry.description,
                    published=published_str,
                    author=getattr(entry, 'author', source_key),
                    vote=vote
                )
            )

    # Sort by date descending
    final_feed = sorted(
        final_feed, key=lambda post: post.published, reverse=True
    )

    # Dump to JSON
    json_object = json.dumps(
        [post.model_dump() for post in final_feed],
        indent=4
    )
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
