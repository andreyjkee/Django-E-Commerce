# -*- coding: utf-8 -*-
#!/usr/bin/env python
import httplib

from django.core import urlresolvers
from django.test import TestCase
from django.test.client import Client

from models import Category


class CatalogTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_view_homepage(self):
		"""Тестирование доступности главной страницы"""
		home_url = urlresolvers.reverse('catalog_home')
		response = self.client.get(home_url)
		# проверяем что получен ответ
		self.failUnless(response)
		# проверяем статус ответа от сервера
		self.assertEqual(response.status_code, httplib.OK)

	def test_view_category(self):
		"""Тестирование доступности просмотра категории"""
		category = Category.objects.all()[0]
		#category = Category.is_active.all()[0]
		category_url = category.get_absolute_url()
		response = self.client.get(category_url)
		self.failUnless(response)
		self.assertEqual(response.status_code, httplib.OK)
		# self.assertEqual(Category.objects.all().count(), 0)
