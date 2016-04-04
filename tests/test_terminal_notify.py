import nose.tools as nt
import os
import feedparser
import sys
sys.path.append("yuan")
import terminal_notify

EXAMPLE_RSS = os.path.join(os.path.dirname(__file__),
                           "../random_shit/example-rss.xml")


def test_get_most_recent_update_link():
    with open(EXAMPLE_RSS) as f:
        xml_string = f.read()
    parsed_feed = feedparser.parse(xml_string)
    result = terminal_notify.get_most_recent_update_link(parsed_feed)
    truth = "http://luckovich.blog.ajc.com/2016/04/01/" + \
        "0403-mike-luckovich-court-order/"
    nt.assert_equal(result, truth)

    if False:
        raise AssertionError("Will fail unsorted!")