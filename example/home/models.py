from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from simple_blog.blocks import CodeBlock, OEmbedBlock, GistBlock, PageListBlock, RichtextBlock
from simple_blog.models import BasePage, Post


class Home(BasePage):
    contents = StreamField(
        [
            ("richtext", RichtextBlock()),
            ("choosen_pages", PageListBlock()),
        ],
        null=True,
        blank=True,
        help_text=_("Contents"),
    )

    template = "home/home.html"
    content_panels = BasePage.content_panels + [
        StreamFieldPanel("contents"),
    ]


class Series(Post):
    contents = StreamField(
        [
            ("richtext", RichtextBlock()),
            ("choosen_pages", PageListBlock()),
            ("embed", OEmbedBlock()),
            ("code", CodeBlock()),
            ("gist", GistBlock()),
        ],
        null=True,
        blank=True,
        help_text=_("Contents"),
    )

    icon_class = "text-box-multiple-outline"
    template = "home/series.html"
    parent_page_types = ["simple_blog.Index"]
    subpage_types = ["simple_blog.Article"]
    content_panels = BasePage.content_panels + [
        StreamFieldPanel("contents"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["items"] = Post.objects.descendant_of(self).live()
        return context
