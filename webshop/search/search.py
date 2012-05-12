# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db.models import Q

from webshop.search.models import SearchTerm
from webshop.catalog.models import Product


STRIP_WORDS = ['a','an','and','by','for','from','in','no','not',
               'of','on','or','that','the','to','with']


def store(request, query):
	"""Сохраняет искомый текст в БД"""
    # если посиковая фраза больше двух символов сохраняем в БД
	if len(query) > 2:
		term = SearchTerm()
		term.query = query
		term.ip_address = request.META.get('REMOTE_ADDR')
		term.user = None
		if request.user.is_authenticated():
		    term.user = request.user
		term.save()

def products(search_text):
    """Извлекает товары содержащие указанный текст"""
    words = _prepare_words(search_text)
    products = Product.active.all()
    results = {}
    results['products'] = []
    # Проходим по всем словам в поисковом запросе
    for word in words:
        products = products.filter(Q(name__icontains=word) |
        Q(description__icontains=word) |
        Q(sku__iexact=word) |
        Q(brand__icontains=word) |
        Q(meta_description__icontains=word) |
        Q(meta_keywords__icontains=word))
        results['products'] = products
    return results

def _prepare_words(search_text):
    """Удаляет общие слова перечисленные с списке STRIP_WORDS
    Делает срез поисковой фразы до 5 слов"""
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]
