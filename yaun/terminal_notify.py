import feedparser
import pync

SITES = {"Mike Luckovich": "http://luckovich.blog.ajc.com/"}


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


def check_for_new_update(url, old_update_url):
    """
    Gets all new updates since old_update_url

    returns: new updates in list, sorted newest to oldest
    """
    parsed_feed = get_and_parse(url)
    if get_most_recent_update_link(parsed_feed) == old_update_url:
        return []
    new_updates = []
    # maybe getting updates should be a function?
    for entry in parsed_feed["entries"]:
        if entry["link"] == old_update_url:
            break
        new_updates.append(entry["link"])
    return new_updates


def push_update_single(message, url):
    """
    Handles actual terminal notification
    """
    pync.Notifier.notify(message, title="Yaun", open=url)


def push_updates(site_update_dict):
    for site, updates in site_update_dict.iteritems():
        if len(updates) == 0:
            continue

        if len(updates) == 1:
            message = site + " updated!"
        else:
            message = "%s has %d new updates!" % (site, len(updates))
        push_update_single(message, updates[0])  # url of most recent


class Feed(object):
    def __init__(self):
        # most recent
        # sites
        pass

    def check_and_push(self):
        # check : check
        # mutate : pending
        # push : check
        pass




