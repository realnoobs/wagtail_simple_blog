from django.utils.translation import gettext_lazy as _
from wagtail.core.models import Page
from simple_blog.models import BaseIndex, Post


class HomePage(Page):
    pass


class NewsIndex(BaseIndex):
    subpage_types = ["home.News"]

    class Meta:
        verbose_name = _("News")


class News(Post):
    index_page_class = NewsIndex
    parent_page_types = ["home.NewsIndex"]
    subpage_types = []
