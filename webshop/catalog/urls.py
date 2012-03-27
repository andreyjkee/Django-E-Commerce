# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url


urlpatterns = patterns('webshop.catalog.views',
	# Главная страница
	url(r'^$', 'index_view',
		{'template_name':'catalog/index.html'},
		name='catalog_home'),
	# Просмотр категории
	url(r'^category/(?P<category_slug>[-\w]+)/$', 'category_view',
		{'template_name':'catalog/category.html'},
		name='catalog_category'),
	# Просмотр товара
	url(r'^product/(?P<product_slug>[-\w]+)/$', 'product_view',
		{'template_name':'catalog/product.html'},
		name='catalog_product'),

)
