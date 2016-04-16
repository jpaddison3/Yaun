from django.views import generic

from .models import Feed


class IndexView(generic.ListView):
    template_name = 'feed_notify/index.html'
    context_object_name = 'updates'

    def get_queryset(self):
        return Feed.objects.last().check_update()
