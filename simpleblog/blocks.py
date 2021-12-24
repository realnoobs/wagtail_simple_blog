from django.core.validators import validate_slug
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.core.blocks.field_block import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    PageChooserBlock,
    RichTextBlock,
    TextBlock,
)

from wagtail.core.blocks.struct_block import StructBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.embeds.blocks import EmbedBlock


table_options = {
    "minSpareRows": 0,
    "startRows": 3,
    "startCols": 3,
    "colHeaders": False,
    "rowHeaders": False,
    "contextMenu": [
        "row_above",
        "row_below",
        "---------",
        "col_left",
        "col_right",
        "---------",
        "remove_row",
        "remove_col",
        "---------",
        "undo",
        "redo",
    ],
    "editor": "text",
    "stretchH": "all",
    "height": 108,
    "renderer": "text",
    "autoColumnSize": False,
}


class CodeBlock(StructBlock):
    language = CharBlock(required=True)
    filename = CharBlock(required=False)
    caption = TextBlock(required=False)
    code = TextBlock(required=True)

    class Meta:
        icon = "code"
        template = "streamblocks/code_block.html"
        group = "Content Blocks"


class GistBlock(StructBlock):
    id = CharBlock(required=True)
    file = CharBlock(
        required=False,
        help_text=_("If the gist has multiple files, specify the filename you want to show"),
    )
    line = CharBlock(
        required=False,
        help_text=_("Line numbers you want to show. The rest are removed. 1-3 or 1,2,3 or 2-"),
    )
    highlight_line = CharBlock(
        required=False,
        help_text=_("Line numbers you want to highlight. Uses the same syntax for line ranges as line"),
    )
    hide_footer = BooleanBlock(
        required=False,
        help_text=_("Removes the gist footer"),
    )
    caption = TextBlock(
        required=False,
        help_text=_("Places a header above the gist with your chosen caption string"),
    )

    class Meta:
        icon = "code"
        template = "streamblocks/gist_block.html"
        group = "Embed Media Blocks"


class OEmbedBlock(StructBlock):
    name = CharBlock(validators=[validate_slug])
    caption = CharBlock(required=False)
    embed = EmbedBlock(max_width=800, max_height=400)

    class Meta:
        icon = "link"
        template = "streamblocks/oembed_block.html"
        group = "Embed Media Blocks"


class RichtextBlock(RichTextBlock):
    class Meta:
        icon = "doc-full"
        template = "streamblocks/richtext_block.html"


class CustomTableBlock(TableBlock):

    STRIPED = "striped"
    BORDER = "border"
    BORDERLESS = "borderless"
    TABLE_STYLE = (
        (STRIPED, "Striped"),
        (BORDER, "Border"),
        (BORDERLESS, "Borderless"),
    )
    style = ChoiceBlock(choices=TABLE_STYLE, default=STRIPED)

    class Meta:
        template = "streamblocks/table_block.html"
        group = "Content Blocks"


class PostChooserBlock(PageChooserBlock):
    class Meta:
        template = "streamblocks/post_block.html"
        group = "Content Blocks"


class HTMLBlock(TextBlock):
    def render(self, value, context=None):
        return mark_safe(value)


REGISTERED_BLOCKS = [
    ("richtext", RichtextBlock()),
    ("html", HTMLBlock()),
    ("codeblock", CodeBlock()),
    ("post_chooser", PostChooserBlock(page_type="simpleblog.Post")),
    ("oembed", OEmbedBlock()),
    ("gist_embed", GistBlock()),
    ("table", CustomTableBlock(table_options=table_options)),
]
