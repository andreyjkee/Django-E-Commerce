# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls.defaults import patterns


urlpatterns = patterns('webshop.catalog.views',
	# Главная страница
	(r'^$', 'index', {'template_name':'catalog/index.html'}, 'catalog_home'),
	# Просмотр категории
	(r'^category/(?P<category_slug>[-\w]+)/$',
		'show_category', {
		'template_name':'catalog/category.html'}, 'catalog_category'),
	# Просмотр товара
	(r'^product/(?P<product_slug>[-\w]+)/$',
		'show_product', {
		'template_name':'catalog/product.html'}, 'catalog_product'),
)