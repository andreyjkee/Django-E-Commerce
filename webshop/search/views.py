# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from webshop.search import search
from webshop import settings


def results_view(request, template_name="search/results.html"):
    """Представление для результатов поиска"""
    # Получаем номер текущей страницы. Устанавливаем 1 если не найдена
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    # получаем поисковую фразу
    query = request.GET.get('query', '')
    print query
    # возвращаем найденные продукты
    matching = search.products(query).get('products')
    # Создаем объект класса Paginator
    paginator = Paginator(matching, settings.PRODUCTS_PER_PAGE)
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
    # Сохраняем поисковую фразу
    search.store(request, query)
    page_title = 'Search Results for: ' + query
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))
