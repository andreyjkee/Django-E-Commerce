# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import template
from django.contrib.flatpages.models import FlatPage

from webshop.cart import cart
from webshop.catalog.models import Category


register = template.Library()

@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
	"""Вставка для виджета отображающего количество разных товаров в корзине"""
	cart_item_count = cart.cart_distinct_item_count(request)
	return {'cart_item_count': cart_item_count }

@register.inclusion_tag("tags/category_list.html")
def categories_tree(request):
	"""Возвращает дерево категорий"""
	return {'nodes': Category.objects.filter(is_active=True) }

@register.inclusion_tag("tags/footer.html")
def footer_links():
	"Вставка для виджета отображающего ссылки на статические страницы внизу"
	flatpage_list = FlatPage.objects.all()
	return {'flatpage_list': flatpage_list }
