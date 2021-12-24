from django.db import models
from django.apps import apps
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.core.paginator import InvalidPage, Paginator
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin import edit_handlers as handlers
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from taggit.models import TaggedItemBase, Tag

from .utils import get_ip, unique_slugify, make_fragment_key
from .blocks import REGISTERED_BLOCKS
from .settings import simpleblog_settings as blog_settings


@register_snippet
class Category(MPTTModel):

    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="childrens",
        help_text=_(
            "Categories and Menu Item, unlike tags, they can have a hierarchy. You might have a "
            "Jazz Item, and under that have children items for Bebop"
            " and Big Band. Totally optional."
        ),
    )
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[
            MinLengthValidator(3),
        ],
        verbose_name=_("Name"),
    )
    icon = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=_("Icon name"),
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        max_length=80,
    )
    description = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
    )

    panels = [
        ImageChooserPanel("thumbnail"),
        handlers.FieldPanel("parent"),
        handlers.FieldPanel("icon"),
        handlers.FieldPanel("name"),
        handlers.FieldPanel("slug"),
        handlers.RichTextFieldPanel("description"),
    ]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    @property
    def opts(self):
        return self._meta

    def __str__(self):
        return str(self.name)

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent category cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


class TaggedPost(TaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        related_name="post_items",
        on_delete=models.CASCADE,
    )
    content_object = ParentalKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="tagged_items",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Post Tag")
        verbose_name_plural = _("Post Tags")


class BasePage(Page):
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    summary = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("Summary"),
    )

    custom_template = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    custom_styles = models.TextField(
        null=True,
        blank=True,
    )
    custom_scripts = models.TextField(
        null=True,
        blank=True,
    )

    show_comments = models.BooleanField(
        default=True,
        help_text=_(
            "Show all comments",
        ),
    )
    allow_comments = models.BooleanField(
        default=True,
        help_text=_("Allow visitors to comments"),
    )
    view_count = models.IntegerField(
        default=0,
        editable=False,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("thumbnail"),
        handlers.FieldPanel("summary"),
    ]
    promote_panels = Page.promote_panels
    design_panels = [
        handlers.FieldPanel("custom_template"),
        handlers.FieldPanel("custom_styles"),
        handlers.FieldPanel("custom_scripts"),
    ]
    settings_panels = Page.settings_panels + [
        handlers.MultiFieldPanel(
            [
                handlers.FieldPanel("show_comments"),
                handlers.FieldPanel("allow_comments"),
            ],
            _("Comments"),
        ),
    ]

    card_type = "article"

    class Meta:
        abstract = True

    @property
    def opts(self):
        return self.specific._meta

    @classmethod
    def get_edit_handler(cls):
        edit_handler = handlers.TabbedInterface(
            [
                handlers.ObjectList(
                    cls.content_panels,
                    heading="Content",
                    classname="contents",
                ),
                handlers.ObjectList(
                    cls.promote_panels,
                    heading="Promote",
                    classname="promotes",
                ),
                handlers.ObjectList(
                    cls.design_panels,
                    heading="Design",
                    classname="design",
                ),
                handlers.ObjectList(
                    cls.settings_panels,
                    heading="Settings",
                    classname="settings",
                ),
            ]
        )
        return edit_handler.bind_to(model=cls)

    def full_clean(self, *args, **kwargs):
        if self.custom_template:
            try:
                get_template(self.custom_template)
            except TemplateDoesNotExist as err:
                raise ValidationError({"custom_template": err})
        return super().full_clean(*args, **kwargs)

    def get_template(self, *args, **kwargs):
        if self.custom_template:
            self.template = self.custom_template
        return self.template

    def get_cache_key(self, request=None):
        req = request
        return make_fragment_key(self.__class__, request=req, page_id=self.id)

    def get_cache_timeout(self):
        return getattr(self, "cache_timeout", blog_settings.PAGE_CACHE_TIMEOUT)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blog_settings"] = blog_settings
        return context

    def get_response(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name=self.get_template(request, *args, **kwargs),
            context=self.get_context(request, *args, **kwargs),
            using=None,
        )

    def handle_view_count(self):
        """Handle page view count using cache"""
        # get ip from request
        ip_address = get_ip(self.request)
        cache_key = "%s:%s:%s" % (ip_address, self.specific.__class__, self.id)
        cache_timeout = 60 * 60 * 24
        visitor = cache.get(cache_key)
        if not visitor:
            self.view_count += 1
            self.save()
            cache.set(cache_key, ip_address, cache_timeout)

    def serve(self, request, *args, **kwargs):
        self.request = request
        self.request.is_preview = getattr(request, 'is_preview', False)
        self.handle_view_count()
        return self.get_response(self.request, *args, **kwargs)

    # def serve(self, request, *args, **kwargs):
    #     """Enhanced  page.serve() with caching"""
    #     self.request = request
    #     cache_key = self.get_cache_key(request)
    #     cache_timeout = self.get_cache_timeout()
    #     self.request.is_preview = getattr(self.request, "is_preview", False)

    #     # get fresh response for preview
    #     if self.request.is_preview:
    #         return self.get_response(self.request, *args, **kwargs)

    #     # get from cache first
    #     resp = cache.get(cache_key)
    #     if not resp:
    #         resp = self.get_response(self.request, *args, **kwargs)
    #         cache.set(cache_key, resp, cache_timeout)

    #     # Update View Count by request
    #     self.handle_view_count()

    #     return resp


class BaseIndex(RoutablePageMixin, BasePage):

    post_per_page = models.IntegerField(
        default=4,
        validators=[MinValueValidator(2), MaxValueValidator(20)],
        help_text=_("Number of post shown in each page."),
    )
    paginator_class = Paginator
    paginate_query_param = "page"
    paginate_last_page_strings = ("last",)

    settings_panels = BasePage.settings_panels + [
        handlers.FieldPanel("post_per_page"),
    ]

    class Meta:
        abstract = True

    def get_subpages_map(self):
        maps = dict()
        for pagemodel in self.subpage_types:
            app_name, model = pagemodel.split(".")
            maps[model.lower()] = apps.get_model(app_name, model)
        return maps

    def get_template(self, *args, **kwargs):
        return super().get_template(*args, **kwargs)

    def get_childs(self):
        return (
            Post.objects.descendant_of(self)
            .filter(
                depth=self.depth + 1,
                path__range=self._get_children_path_interval(self.path),
            )
            .order_by("-first_published_at")
            .specific()
            .live()
        )

    def get_paginator_class(self):
        return self.paginator_class

    def get_paginate_by(self):
        return self.post_per_page

    def get_paginated_queryset(self, request, queryset):
        per_page = self.get_paginate_by()
        paginator = self.paginator_class(queryset, per_page=per_page)
        page_number = self.get_page_number(request, paginator)
        try:
            page_object = paginator.page(page_number)
        except InvalidPage as exc:
            raise Http404(exc)
        return page_object

    def get_page_number(self, request, paginator):
        page_number = request.GET.get(self.paginate_query_param, 1)
        if page_number in self.paginate_last_page_strings:
            page_number = paginator.num_pages
        return page_number

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["index"] = self
        context["posts"] = self.posts
        context["currents"] = self.currents
        return context

    @route(r"^tag/(?P<slug>[-\w]+)/$")
    def tagged_posts(self, request, slug, *args, **kwargs):
        queryset = self.get_childs().filter(tags__slug=slug)
        self.posts = self.get_paginated_queryset(request, queryset)
        self.currents = [slug, "tag"]
        self.template = blog_settings.TEMPLATES["TAG"]
        return self.render(request, context_overrides={"tag": slug})

    @route(r"^category/(?P<slug>[-\w]+)/$")
    def categorized_posts(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        cat_ids = [cat.id for cat in category.get_descendants(include_self=True)]
        queryset = self.get_childs().filter(category_id__in=cat_ids)
        self.template = blog_settings.TEMPLATES["CATEGORY"]
        self.posts = self.get_paginated_queryset(request, queryset)
        self.currents = [slug, "category"]
        return self.render(request, context_overrides={"category": category})

    @route(r"^content/(?P<slug>[-\w]+)/$")
    def posttype(self, request, slug, *args, **kwargs):
        types = self.get_subpages_map()
        PageModel = types.get(slug)
        if not PageModel:
            raise Http404("Post type %s doesn't exist" % slug)
        queryset = self.get_childs().exact_type(PageModel)
        self.posts = self.get_paginated_queryset(request, queryset)
        self.currents = [slug, "posttype"]
        return self.render(request)

    @route(r"^$")
    def index(self, request, *args, **kwargs):
        queryset = self.get_childs()
        self.posts = self.get_paginated_queryset(request, queryset)
        self.currents = ["index"]
        return self.render(request)


class Post(BasePage):
    category = models.ForeignKey(
        Category,
        related_name="posts",
        verbose_name=_("category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    tags = ClusterTaggableManager(
        verbose_name=_("tags"),
        through="simpleblog.TaggedPost",
        blank=True,
    )
    featured = models.BooleanField(
        default=False,
        help_text=_("Whether this page will appear featured posts list"),
    )

    icon_class = "text-box-outline"
    index_class = None
    template = blog_settings.TEMPLATES["POST"]
    parent_page_types = blog_settings.POST_PARENTPAGE_TYPES
    subpage_types = blog_settings.POST_SUBPAGE_TYPES

    content_panels = BasePage.content_panels + [
        handlers.MultiFieldPanel(
            [
                handlers.FieldPanel("tags"),
                handlers.FieldPanel("category"),
            ],
            _("Category & Tags"),
        ),
    ]
    promote_panels = Page.promote_panels + [
        handlers.MultiFieldPanel(
            children=[handlers.FieldPanel("featured")],
            heading=_("Others "),
        )
    ]

    class Meta:
        ordering = ("-first_published_at",)

    @classmethod
    def check(cls, **kwargs):
        # index class for Post subclass must be subclass of simpleblog.BaseIndex
        if cls.index_class and not issubclass(cls.index_class, BaseIndex):
            raise ImproperlyConfigured(
                "%s index_class property must be simpleblog.BaseIndex subclass!" % cls.__name__
            )
        errors = super().check(**kwargs)
        return errors

    def get_index_class(self):
        return self.index_class or Index

    def get_index_page(self):
        index = self.get_ancestors().exact_type(self.get_index_class()).first().specific
        return index

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["index"] = self.get_index_page()
        context["prev"] = self.get_prev_siblings().live().first()
        context["next"] = self.get_next_siblings().live().first()
        context["currents"] = []
        return context


class Article(Post):
    contents = StreamField(
        REGISTERED_BLOCKS,
        null=True,
        blank=True,
        help_text=_("Contents"),
    )
    template = blog_settings.TEMPLATES["ARTICLE"]
    parent_page_types = blog_settings.ARTICLE_PARENTPAGE_TYPES
    subpage_types = blog_settings.ARTICLE_SUBPAGE_TYPES

    content_panels = Post.content_panels + [
        handlers.StreamFieldPanel("contents"),
    ]


class Index(BaseIndex):

    contents = StreamField(
        REGISTERED_BLOCKS,
        null=True,
        blank=True,
        help_text=_("Contents"),
    )

    child_class = Post
    template = blog_settings.TEMPLATES["INDEX"]
    parent_page_types = blog_settings.INDEX_PARENTPAGE_TYPES
    subpage_types = blog_settings.INDEX_SUBPAGE_TYPES

    content_panels = BasePage.content_panels + [
        handlers.StreamFieldPanel("contents"),
    ]

    class Meta:
        verbose_name = _("Index")
