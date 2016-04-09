import nose.tools as nt
import os
import feedparser
import mock
import sys
sys.path.append("yaun")
import terminal_notify

EXAMPLE_RSS = os.path.join(os.path.dirname(__file__),
                           "../random_shit/example-rss.xml")
EXAMPLE_URL = "http://luckovich.blog.ajc.com/feed/"


def test_get_and_parse():
    # how do we test code that hits a changing network?
    # should get back a FeedParserDict
    # with correct name
    # should have a place for most recent links
    result = terminal_notify.get_and_parse(EXAMPLE_URL)
    nt.assert_in("Mike Luckovich", result["feed"]["title"])
    nt.assert_not_equal(result["entries"][0]["link"], None)


def test_get_most_recent_update_link():
    with open(EXAMPLE_RSS) as f:
        xml_string = f.read()
    parsed_feed = feedparser.parse(xml_string)
    result = terminal_notify.get_most_recent_update_link(parsed_feed)
    truth = "http://luckovich.blog.ajc.com/2016/04/01/" + \
        "0403-mike-luckovich-court-order/"
    nt.assert_equal(result, truth)

    if False:
        # TODO
        raise AssertionError("Will fail unsorted!")


@mock.patch("terminal_notify.get_and_parse")
def test_check_for_new_update(get_and_parse_mock):
    # --- it returns empty list on no update
    m = mock.Mock()
    # return value should be parsed example url TODO
    get_and_parse_mock.return_value = {
        "entries": [
            {"link": "bar"}
        ]
    }
    result = terminal_notify.check_for_new_update("foo", "bar")
    truth = []
    nt.assert_equal(result, truth)

    # --- it returns all newer links on update
    get_and_parse_mock.return_value = {
        "entries": [
            {"link": "ar"},
            {"link": "aar"},
            {"link": "bar"}
        ]
    }
    result = terminal_notify.check_for_new_update("foo", "bar")
    truth = ["ar", "aar"]
    nt.assert_equal(result, truth)


@mock.patch("terminal_notify.pync")
def test_push_update(pync_mock):
    terminal_notify.push_update("Mike Luckovich", "http://ajc.com/foo")
    pync_mock.Notifier.notify.assert_called_with(
        "Mike Luckovich", title="Yaun", open="http://ajc.com/foo")







