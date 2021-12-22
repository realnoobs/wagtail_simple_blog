from simple_blog.models import Category, Post, Tag
from django.template import Library
from django.template.loader import get_template, select_template
from django.utils.translation import gettext_lazy as _
from simple_blog.utils import get_gravatar_url

register = Library()


@register.simple_tag(takes_context=False, name="nice_username")
def nice_username(user):
    return user.get_full_name() or user.username


@register.inclusion_tag("components/social_share.html", takes_context=True)
def social_share_widget(context, object_title, object_or_url, title="Share this"):
    return {
        "title": title,
        "object_title": object_title,
        "object_or_url": object_or_url,
    }


@register.inclusion_tag("components/tags_list.html", takes_context=True)
def tags_list(context, index, number=20, **kwargs):
    title = kwargs.get("title", None) or _("Tags")
    tags = Tag.objects.all()[:number]
    return {
        "title": title,
        "request": context["request"],
        "index": index,
        "tags": tags,
    }


@register.inclusion_tag("components/categories_list.html", takes_context=True)
def categories_list(context, index, number=20, **kwargs):
    title = kwargs.get("title", None) or _("Categories")
    categories = Category.objects.all()[:number]
    return {
        "title": title,
        "request": context["request"],
        "index": index,
        "currents": context["currents"],
        "categories": categories,
    }


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
        kwargs["title"] = _("Related %s") % index.opts.verbose_name
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
        kwargs["title"] = _("Related %s") % index.opts.verbose_name
    template = template_name or "components/post_list.html"
    tags = [t.id for t in post.tags.all()]
    queryset = Post.objects.descendant_of(index).filter(tags__id__in=tags).exclude(id=post.id).live()[:limit]
    return render_posts_list(request, queryset, template, **kwargs)


@register.simple_tag(takes_context=True, name="recent_posts")
def recent_posts(context, index, limit=5, template_name=None, **kwargs):
    request = context["request"]
    title = kwargs.get("title", None)
    if not title:
        kwargs["title"] = _("Recent %s") % index.opts.verbose_name
    template = template_name or "components/post_list.html"
    queryset = Post.objects.descendant_of(index).order_by("-first_published_at").live()[:limit]
    return render_posts_list(request, queryset, template, **kwargs)


@register.simple_tag(takes_context=True, name="popular_posts")
def popular_posts(context, index, limit=5, template_name=None, **kwargs):
    request = context["request"]
    title = kwargs.get("title", None)
    if not title:
        kwargs["title"] = _("Popular %s") % index.opts.verbose_name
    template = template_name or "components/post_list.html"
    queryset = Post.objects.descendant_of(index).order_by("-view_count").live()[:limit]
    return render_posts_list(request, queryset, template, **kwargs)


@register.simple_tag(takes_context=True, name="featured_posts")
def featured_posts(context, index, limit=5, template_name=None, **kwargs):
    request = context["request"]
    title = kwargs.get("title", None)
    if not title:
        kwargs["title"] = _("Featured %s") % index.opts.verbose_name
    template = template_name or "components/post_list.html"
    queryset = Post.objects.descendant_of(index).filter(featured=True).live()[:limit]
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
def render_post(context, blog, post):
    request = context["request"]
    template = select_template(
        [
            "simple_blog/content_%s.html" % post.opts.model_name,
            "simple_blog/content.html",
        ]
    )
    return template.render({"blog": blog, "post": post, "request": request}, request)
