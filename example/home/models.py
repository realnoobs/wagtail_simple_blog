from django.utils.translation import gettext_lazy as _
from simple_blog.models import BasePage


class HomePage(BasePage):
    pass


# class Series(Post):

#     template = "simple_blog/series.html"
#     parent_page_types = ["simple_blog.Index"]
#     subpage_types = ["simple_blog.Article"]

#     def get_context(self, request, *args, **kwargs):
#         context = super().get_context(request, *args, **kwargs)
#         context["items"] = Post.objects.descendant_of(self).live()
#         return context


# class NewsIndex(BaseIndex):
#     subpage_types = ["home.News"]

#     class Meta:
#         verbose_name = _("News")


# class News(Post):
#     index_page_class = NewsIndex
#     parent_page_types = ["home.NewsIndex"]
#     subpage_types = []
