from wagtail.core.models import Page
from simple_blog.models import BaseIndex, Post


class HomePage(Page):
    pass


class NewsIndex(BaseIndex):
    subpage_types = ["home.News"]


class News(Post):
    parent_page_types = ["home.NewsIndex"]
    subpage_types = []
