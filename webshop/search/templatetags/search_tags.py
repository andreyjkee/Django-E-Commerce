# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib

from django import template

from webshop.search.forms import SearchForm


register = template.Library()


@register.inclusion_tag("tags/search_box.html")
def search_box(request):
    """Вставка для отображения формы поиска"""
    query = request.GET.get('query','')
    form = SearchForm({'query': query })
    return {'form': form }

@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request, paginator):
    """Вставка для постраничного вывода"""
    raw_params = request.GET.copy()
    page = raw_params.get('page', 1)
    p = paginator.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    params = urllib.urlencode(raw_params)
    return {'request': request,
            'paginator': paginator,
            'p': p,
            'params': params }
