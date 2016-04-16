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
        new_updates.append(entry["link"])
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


def push_update_single(message, url):
    """
    Handles actual terminal notification
    """
    pync.Notifier.notify(message, title="Yaun", open=url)


def push_updates(site_update_dict):
    """
    Push updates for all sites
    """
    for site, updates in site_update_dict.iteritems():
        if len(updates) == 0:
            continue

        if len(updates) == 1:
            message = site + " updated!"
        else:
            # TODO: should redirect to feed instead of post on >1
            message = "%s has %d new updates!" % (site, len(updates))
        push_update_single(message, updates[0])  # url of most recent


class Feed(object):
    """
    Keeps track of feed state
    """
    def __init__(self, sites_dict, most_recent_dict):
        """
        sites_dict, site names: feed urls
        most_recent_dict, site names: most recent link urls
        """
        # TODO need handling for dict keys unequal
        self.sites_dict = sites_dict
        self.most_recent_dict = most_recent_dict

    def _set_most_recent(self, updates_dict):
        """
        Update most recent urls
        """
        for site, updates in updates_dict.iteritems():
            if len(updates) > 0:
                self.most_recent_dict[site] = updates[0]

    def check_and_push(self):
        """
        Checks for and notifies user of updates
        """
        updates_dict = check_updates(self.sites_dict, self.most_recent_dict)
        push_updates(updates_dict)
        self._set_most_recent(updates_dict)


if __name__ == "__main__":
    most_recent = {SITES.keys()[0]: "None"}
    feed = Feed(SITES, most_recent)

    minutes_between = 10
    while True:
        print "checking for updates!"
        feed.check_and_push()
        time.sleep(minutes_between * 60)
