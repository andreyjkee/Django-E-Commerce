# -*- coding: utf-8 -*-
#!/usr/bin/env python
import httplib

from django.core import urlresolvers
from django.test import TestCase
from django.test.client import Client
#from django.views.defaults import page_not_found

from webshop.catalog.models import Category, Product


class CatalogTest(TestCase):
	def setUp(self):
		self.client = Client()

	@staticmethod
	def get_template_name(url):
		"""Получение названия шаблона из url"""
		# >>> urlresolvers.resolve('/product/something/')
		# (<function show_product at 0x11e0488>, (),
		#    {'template_name': 'catalog/product.html', 'product_slug': 'some-product'})
		# >>> urlresolvers.resolve('/product/something/')[2]['template_name']
		# 'catalog/product.html' 
		url_entry = urlresolvers.resolve(url)
		return url_entry[2]['template_name']

	def test_view_homepage(self):
		"""Тестирование доступности главной страницы"""
		home_url = urlresolvers.reverse('catalog_home')
		response = self.client.get(home_url)
		template_name = self.get_template_name(home_url)
		# проверяем что получен ответ
		self.failUnless(response)
		# проверяем статус ответа от сервера
		self.assertEqual(response.status_code, httplib.OK)
		self.assertTemplateUsed(response, template_name)

	def test_view_category(self):
		"""Тестирование доступности просмотра категории"""
		category = Category.objects.all()[0]
		#category = Category.is_active.all()[0]
		category_url = category.get_absolute_url()
		template_name = self.get_template_name(category_url)
		response = self.client.get(category_url)
		self.failUnless(response)
		self.assertEqual(response.status_code, httplib.OK)
		self.assertTemplateUsed(response, template_name)
		# проверяем что страница содержит информацию о категории 
		self.assertContains(response, category.name) 
		self.assertContains(response, category.description)

	def test_view_product(self):
		"""Тестирование доступности просмотра категории"""
		product = Product.objects.all()[0]
		product_url = product.get_absolute_url()
		template_name = self.get_template_name(product_url)
		response = self.client.get(product_url)
		self.failUnless(response)
		self.assertEqual(response.status_code, httplib.OK)
		self.assertTemplateUsed(response, template_name)
		# проверяем что страница содержит информацию о товаре
		self.assertContains(response, product.name) 
		self.assertContains(response, product.price)
		self.assertContains(response, product.description)

	# def test_inactive_product_returns_404(self):
	# 	"""Проверка что не активный товар не отображается на сайте"""
	# 	inactive_product = Product.objects.filter(is_active=False)[0]
	# 	inactive_product_url = inactive_product.get_absolute_url()
	# 	template_name = self.get_template_name(inactive_product_url)
	# 	# получаем название шаблона используемого django для 404 по умолчанию
	# 	#django_404_template = page_not_found.func_defaults[0]
	# 	response = self.client.get(inactive_product_url)
	# 	#self.assertTemplateUsed(response, django_404_template)
	# 	self.assertTemplateNotUsed(response, template_name)
