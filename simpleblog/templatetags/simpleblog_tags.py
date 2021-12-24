from django import template
from django.template import Library
from django.template.loader import get_template, select_template
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from wagtail.images.models import Filter
from wagtail.images.shortcuts import get_rendition_or_not_found

from simpleblog.models import Category, Post, Tag
from simpleblog.utils import get_gravatar_url

register = Library()


@register.simple_tag(takes_context=False, name="nice_username")
def nice_username(user):
    return user.get_full_name() or user.username


@register.simple_tag(takes_context=True, name="social_share_widget")
def social_share_widget(context, object_title, object_url, template_name=None, **kwargs):
    title = kwargs.get("title", None) or _("Tags")
    template = get_template(template_name or "components/tags_list.html")
    kwargs.update(
        {
            "title": title,
            "object_title": object_title,
            "object_or_url": object_url,
        }
    )
    return template.render(kwargs, context["request"])


@register.simple_tag(takes_context=True, name="tags_list")
def tags_list(context, index, number=20, template_name=None, **kwargs):
    title = kwargs.get("title", None) or _("Tags")
    tags = Tag.objects.all()[:number]
    template = get_template(template_name or "components/tags_list.html")
    kwargs.update(
        {
            "title": title,
            "request": context["request"],
            "index": index,
            "tags": tags,
        }
    )
    return template.render(kwargs, context["request"])


@register.simple_tag(takes_context=True, name="categories_list")
def categories_list(context, index, number=20, template_name=None, **kwargs):
    title = kwargs.get("title", None) or _("Categories")
    categories = Category.objects.all()[:number]
    template = get_template(template_name or "components/categories_list.html")
    kwargs.update(
        {
            "title": title,
            "index": index,
            "request": context["request"],
            "currents": context["currents"],
            "categories": categories,
        }
    )
    return template.render(kwargs, context["request"])


@register.simple_tag(takes_context=True, name="posttypes_list")
def posttypes_list(context, index, template_name=None, **kwargs):
    title = kwargs.get("title", None) or _("Contents")
    template = get_template(template_name or "components/post_type_list.html")
    posttypes = [(slug, model.icon_class)for slug, model in index.get_subpages_map().items()]
    kwargs.update(
        {
            "title": title,
            "index": index,
            "posttypes": posttypes,
            "request": context["request"],
            "currents": context["currents"],
        }
    )
    return template.render(kwargs, context["request"])


def render_posts_list(request, queryset, template_name, **kwargs):
    kwargs.update({"post_list": queryset})
    template = get_template(template_name)
    return template.render(kwargs, request)


@register.simple_tag(takes_context=True, name="related_posts_by_category")
def related_posts_by_category(context, index, post, limit=5, template_name=None, **kwargs):
    request = context["request"]
    template = template_name or "components/post_list.html"
    title = kwargs.get("title", None)
    if not title:
        kwargs["title"] = _("Related %s") % index.child_class._meta.verbose_name
    category = getattr(post, "category", None)
    queryset = []
    if category:
        categories = [cat.id for cat in post.category.get_descendants(include_self=True)]
        queryset = (
            Post.objects.descendant_of(index)
            .filter(category__in=categories)
            .exclude(id=post.id)
            .live()[:limit]
        )
    return render_posts_list(request, queryset, template, **kwargs)


@register.simple_tag(takes_context=True, name="related_posts_by_tags")
def related_posts_by_tags(context, index, post, limit=5, template_name=None, **kwargs):
    request = context["request"]
    title = kwargs.get("title", None)
    if not title:
        kwargs["title"] = _("Related %s") % index.child_class._meta.verbose_name
    template = template_name or "components/post_list.html"
    tags = [t.id for t in post.tags.all()]
    queryset = Post.objects.descendant_of(index).filter(tags__id__in=tags).exclude(id=post.id).live()[:limit]
    return render_posts_list(request, queryset, template, **kwargs)


@register.simple_tag(takes_context=True, name="recent_posts")
def recent_posts(context, index=None, limit=5, template_name=None, **kwargs):
    request = context["request"]
    title = kwargs.get("title", None)
    if not title:
        kwargs["title"] = _("Recent %s") % index.child_class._meta.verbose_name
    template = template_name or "components/post_list.html"
    queryset = Post.objects
    if index:
        queryset = queryset.descendant_of(index)
    queryset = queryset.order_by("-first_published_at").live()[:limit]
    return render_posts_list(request, queryset, template, **kwargs)


@register.simple_tag(takes_context=True, name="popular_posts")
def popular_posts(context, index=None, limit=5, template_name=None, **kwargs):
    request = context["request"]
    title = kwargs.get("title", None)
    if not title:
        kwargs["title"] = _("Popular %s") % index.child_class._meta.verbose_name
    template = template_name or "components/post_list.html"
    queryset = Post.objects
    if index:
        queryset = queryset.descendant_of(index)
    queryset = queryset.order_by("-view_count").live()[:limit]
    return render_posts_list(request, queryset, template, **kwargs)


@register.simple_tag(takes_context=True, name="featured_posts")
def featured_posts(context, index=None, limit=5, template_name=None, **kwargs):
    request = context["request"]
    title = kwargs.get("title", None)
    if not title:
        kwargs["title"] = _("Featured %s") % index.child_class._meta.verbose_name
    template = template_name or "components/post_list.html"
    queryset = Post.objects
    if index:
        queryset = queryset.descendant_of(index)
    queryset = queryset.filter(featured=True).live()[:limit]
    return render_posts_list(request, queryset, template, **kwargs)


@register.simple_tag(takes_context=True)
def gravatar_url(context, user, size=50):
    return get_gravatar_url(user.email, size=size)


@register.filter(name="proper_paginate")
def proper_paginate(paginator, current_page, neighbors=10):

    if paginator.num_pages > 2 * neighbors:
        start_index = max(1, current_page - neighbors)
        end_index = min(paginator.num_pages, current_page + neighbors)
        if end_index < start_index + 2 * neighbors:
            end_index = start_index + 2 * neighbors
        elif start_index > end_index - 2 * neighbors:
            start_index = end_index - 2 * neighbors
        if start_index < 1:
            end_index -= start_index
            start_index = 1
        elif end_index > paginator.num_pages:
            start_index -= end_index - paginator.num_pages
            end_index = paginator.num_pages
        page_list = [f for f in range(start_index, end_index + 1)]
        return page_list[: (2 * neighbors + 1)]
    return paginator.page_range


@register.simple_tag(takes_context=True)
def replace_param(context, **kwargs):
    """ """
    d = context["request"].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag(takes_context=True, name="render_post")
def render_post(context, index, post):
    request = context["request"]
    template = select_template(
        [
            "simpleblog/content_%s.html" % post.opts.model_name,
            "simpleblog/content.html",
        ]
    )
    return template.render({"index": index, "post": post, "request": request}, request)


@register.simple_tag(takes_context=True, name="thumbnailer")
def thumbnailer(context, img, filter="fill", width=370, height=210, output_var="thumbnail", **kwargs):
    filter_spec = "%s-%sx%s" % (filter, width, height)
    return ImageNode(img, filter_spec, output_var=output_var, attrs=kwargs).render(context)


class ImageNode(template.Node):
    def __init__(self, img, filter_spec, output_var, attrs={}):
        self.image = img
        self.output_var = output_var
        self.attrs = attrs
        self.filter_spec = filter_spec

    @cached_property
    def filter(self):
        return Filter(spec=self.filter_spec)

    def render(self, context):
        image = self.image

        if not hasattr(image, "get_rendition"):
            raise ValueError("image tag expected an Image object, got %r" % image)

        rendition = get_rendition_or_not_found(image, self.filter)

        if self.output_var:
            # return the rendition object in the given variable
            context[self.output_var] = rendition
            return ""
        else:
            # render the rendition's image tag now
            resolved_attrs = {}
            for key in self.attrs:
                resolved_attrs[key] = self.attrs[key].resolve(context)
            return rendition.img_tag(resolved_attrs)
