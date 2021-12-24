from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.search.models import Query

from simpleblog.models import Post
from .settings import simpleblog_settings as blog_settings


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Post.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Post.objects.none()

    # Pagination
    paginator = Paginator(search_results, per_page=blog_settings.SEARCH_ITEMS_PER_PAGE)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        blog_settings.TEMPLATES["SEARCH"],
        {"search_query": search_query, "search_results": search_results, "currents": ["search"]},
    )
