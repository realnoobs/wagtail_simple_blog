from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from simpleblog.blocks import REGISTERED_BLOCKS
from simpleblog.models import BasePage, Post


class Home(BasePage):
    contents = StreamField(
        REGISTERED_BLOCKS,
        null=True,
        blank=True,
        help_text=_("Contents"),
    )

    template = "home.html"
    content_panels = BasePage.content_panels + [
        StreamFieldPanel("contents"),
    ]


class Series(Post):
    contents = StreamField(
        REGISTERED_BLOCKS,
        null=True,
        blank=True,
        help_text=_("Contents"),
    )

    icon_class = "text-box-multiple-outline"
    template = "simpleblog/series.html"
    parent_page_types = ["simpleblog.Index"]
    subpage_types = ["simpleblog.Article"]
    content_panels = BasePage.content_panels + [
        StreamFieldPanel("contents"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["items"] = Post.objects.descendant_of(self).live()
        return context
