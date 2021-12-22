from django.utils.translation import gettext_lazy as _
from wagtail.core.blocks.field_block import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    FloatBlock,
    PageChooserBlock,
    RichTextBlock,
    TextBlock,
    URLBlock,
)
from wagtail.core.blocks.list_block import ListBlock
from wagtail.core.blocks.struct_block import StructBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.embeds.blocks import EmbedBlock
from .settings import simple_blog_settings as blog_settings


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

typed_table = TypedTableBlock(
    [
        ("text", CharBlock()),
        ("numeric", FloatBlock()),
        ("rich_text", RichTextBlock()),
        ("image", ImageChooserBlock()),
        (
            "country",
            ChoiceBlock(
                choices=[
                    ("be", "Belgium"),
                    ("fr", "France"),
                    ("de", "Germany"),
                    ("nl", "Netherlands"),
                    ("pl", "Poland"),
                    ("uk", "United Kingdom"),
                ]
            ),
        ),
    ], group="Content Blocks"
)


class DiagramBlock(StructBlock):
    title = CharBlock(required=True)
    caption = RichTextBlock(required=False)
    code = TextBlock(required=True)

    class Meta:
        icon = "code"
        template = "streamblocks/diagram_block.html"
        group = "Embed Media Blocks"


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
    caption = CharBlock(required=False)
    embed = EmbedBlock(max_width=800, max_height=400)

    class Meta:
        icon = "link"
        template = "streamblocks/oembed_block.html"
        group = "Embed Media Blocks"


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "streamblocks/image_block.html"


class ImageGalleryBlock(StructBlock):
    classnames = CharBlock(required=False)
    images = ListBlock(ImageBlock())

    class Meta:
        icon = "image"
        template = "streamblocks/gallery_block.html"
        group = "Relational Blocks"


class RichtextBlock(RichTextBlock):
    class Meta:
        icon = "doc-full"
        template = "streamblocks/richtext_block.html"
        group = "Content Blocks"


class QuoteBlock(StructBlock):
    quote = TextBlock(required=True)
    author = CharBlock(required=False)
    link = URLBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "streamblocks/quote_block.html"
        group = "Content Blocks"


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


class PageListBlock(StructBlock):
    title = CharBlock(required=False)
    pages = ListBlock(child_block=PageChooserBlock(page_type="simple_blog.Post"))

    class Meta:
        template = "streamblocks/pagelist_block.html"
        group = "Relational Blocks"


REGISTERED_BLOCKS = [
    ("richtext", RichtextBlock()),
    ("quote", QuoteBlock()),
    ("choosen_pages", PageListBlock()),
    ("code", CodeBlock()),
    ("gist", GistBlock()),
    ("diagram", DiagramBlock()),
    ("embed", OEmbedBlock()),
    ("image_gallery", ImageGalleryBlock()),
    ("table", CustomTableBlock(table_options=table_options)),
    ("table_typed", typed_table),
] + blog_settings.EXTRA_STREAMFIELDS
