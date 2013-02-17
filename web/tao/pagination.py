"""
==================
tao.pagination
==================

Helper to paginate a queryset
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings

def paginate(queryset, page, per_page=None):
    if per_page is None:
        per_page = settings.NUM_RECORDS_PER_PAGE

    paginator = Paginator(queryset, per_page)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
