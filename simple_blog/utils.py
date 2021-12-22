import re
import logging
import hashlib
from django.utils.http import urlencode

from django.db import models
from django.apps import apps
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.template.defaultfilters import slugify

logger = logging.getLogger("labirin")


def get_gravatar_url(email, size=50):
    default = "mm"
    size = int(size) * 2  # requested at retina size by default and scaled down at point of use with css
    gravatar_provider_url = "//www.gravatar.com/avatar"

    if (not email) or (gravatar_provider_url is None):
        return None

    gravatar_url = "{gravatar_provider_url}/{hash}?{params}".format(
        gravatar_provider_url=gravatar_provider_url.rstrip("/"),
        hash=hashlib.md5(email.lower().encode("utf-8")).hexdigest(),
        params=urlencode({"s": size, "d": default}),
    )

    return gravatar_url


def get_ip(request):
    """
    Attempts to extract the IP number from the HTTP request headers.
    """
    key = "REMOTE_ADDR"
    meta = request.META

    # Lowercase keys
    simple_meta = {k.lower(): v for k, v in request.META.items()}
    ip = meta.get(key, simple_meta.get(key, "0.0.0.0"))
    return ip


def delete_cache(prefix, user):
    """
    Create key from prefix-user.pk and delete from cache.
    """
    key = f"{prefix}:{user.pk}"

    # Check if it exists and delete object from cache.
    if cache.get(key):
        cache.delete(key)
        logger.debug(f"deleted {key} from cache")
    return


def make_fragment_key(model, request=None, **kwarg):
    """Make Cache Fragment key based on model and request params

    Args:
        model ([type|str]): Model Class or model_name with format `app_label.model_name`
        request ([type], optional): Request. Defaults to None.

    Returns:
        [type]: [description]
    """
    if isinstance(model, str):
        fragment_name = model
    elif issubclass(model, models.Model):
        opts = model._meta
        fragment_name = f"{opts.app_label}.{opts.model_name}"

    vary_on = ["%s:%s" % (key, val) for key, val in kwarg.items()]

    if request is not None:
        vary_on.extend(["%s:%s" % (key, val) for key, val in request.GET.items()])

    cache_key = make_template_fragment_key(fragment_name, vary_on)
    return cache_key


def delete_fragment_cache(model, request=None, **kwargs):
    """
    Drops a fragment cache.
    """
    key = make_fragment_key(model, request=None, **kwargs)
    cache.delete(key)


def delete_page_cache(page, **kwargs):
    """
    Delete specific fragment caches,
    include request=request to varying based on query params

    Args:
        page ([Page]): Page object
    """
    model = apps.get_model(page._meta.app_label, page._meta.model_name, require_ready=False)
    delete_fragment_cache(model=model, page_id=page.id, **kwargs)
    if page.parent:
        delete_fragment_cache(model=model, page_id=page.parent.id, **kwargs)


def pluralize(value, word):
    if value > 1:
        return "%d %ss" % (value, word)
    else:
        return "%d %s" % (value, word)


def unique_slugify(instance, value, slug_field_name="slug", queryset=None, slug_separator="-"):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = "%s%s" % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[: slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = "%s%s" % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator="-"):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ""
    if separator == "-" or not separator:
        re_sep = "-"
    else:
        re_sep = "(?:-|%s)" % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub("%s+" % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != "-":
            re_sep = re.escape(separator)
        value = re.sub(r"^%s+|%s+$" % (re_sep, re_sep), "", value)
    return value
