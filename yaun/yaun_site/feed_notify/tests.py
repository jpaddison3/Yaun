import mock
import copy

from django.test import TestCase

from . import models


class FeedTests(TestCase):

    @mock.patch("feed_notify.models.check_update_single")
    def test_check_update_positive(self, update_mock):
        mock_return = ["example.com/1"]
        update_mock.return_value = copy.copy(mock_return)
        feed = models.Feed()
        result = feed.check_update()
        self.assertEqual(result, mock_return)
        self.assertEqual(feed.most_recent_url, mock_return[0])
