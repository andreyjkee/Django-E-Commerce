# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from webshop.catalog.models import Category, Product


def index(request, template_name="catalog/index.html"):
	"""Представление главной страницы"""
	page_title = _(u'Internet Magazine')
	# Функция locals получает все поля словаря
	return render_to_response(template_name, locals(), 
		context_instance=RequestContext(request))
	
def show_category(request, category_slug, 
	template_name="catalog/category.html"):
	"""Представление для просмотра конкретной категории"""
	c = get_object_or_404(Category, slug=category_slug)
	products = c.product_set.all()
	page_title = c.name
	meta_keywords = c.meta_keywords
	meta_description = c.meta_description
	return render_to_response(template_name, locals(), 
		context_instance=RequestContext(request))
	
def show_product(request, product_slug, template_name="catalog/product.html"):
	"""Представление для просмотра конкретного продукта"""
	p = get_object_or_404(Product, slug=product_slug)
	categories = p.categories.filter(is_active=True)
	page_title = p.name
	meta_keywords = p.meta_keywords
	meta_description = p.meta_description
	return render_to_response(template_name, locals(), 
		context_instance=RequestContext(request))