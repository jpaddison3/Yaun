"""
Get terminal notifications for updated websites

JP Addison
"""
import feedparser
import pync
import time

SITES = {"Mike Luckovich": "http://luckovich.blog.ajc.com/feed/"}


def get_and_parse(url):
    """
    This wrapper to feedparser is a good single exit point in my code
    """
    return feedparser.parse(url)


def get_most_recent_update_link(parsed_feed):
    """
    Extracts the link of the most recent update from a feedparser object

    WARNING, ASSUMES SORTED FEED TODO
    """
    # maybe getting updates should be a function?
    return parsed_feed["entries"][0]["link"]


def check_update_single(url, most_recent_url):
    """
    Gets all new updates since most_recent_url

    returns: new updates in list, sorted newest to oldest
    """
    parsed_feed = get_and_parse(url)
    if get_most_recent_update_link(parsed_feed) == most_recent_url:
        return []
    new_updates = []
    # maybe getting updates should be a function?
    for entry in parsed_feed["entries"]:
        if entry["link"] == most_recent_url:
            break
        new_updates.append({"link": entry["link"], "title": entry["title"],
                            "summary": entry["summary"]})
    return new_updates


def check_updates(sites_dict, most_recent_dict):
    """
    Checks for updates from all sites
    """
    update_dict = {}
    for site, feed_url in sites_dict.iteritems():
        recent_url = most_recent_dict[site]
        update_dict[site] = check_update_single(feed_url, recent_url)
    return update_dict