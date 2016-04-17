from django.db import models

from .feed_functions import check_update_single

class Feed(models.Model):
    site_url = models.CharField(max_length=200)
    most_recent_url = models.CharField(max_length=200)

    def _set_most_recent(self, updates):
        if len(updates) > 0:
            self.most_recent_url = updates[0]["link"]

    def check_update(self):
        """
        Checks for and notifies user of updates
        """
        updates = check_update_single(self.site_url, self.most_recent_url)
        self._set_most_recent(updates)
        self.save()
        return updates
