SITES = ["http://luckovich.blog.ajc.com/"]


def get_most_recent_update_link(parsed_feed):
    """
    Extracts the link of the most recent update from a feedparser object

    WARNING, ASSUMES SORTED FEED TODO
    """
    return parsed_feed["entries"][0]["link"]
