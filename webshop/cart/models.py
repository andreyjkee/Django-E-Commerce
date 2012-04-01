# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal

from django.db import models

from webshop.catalog.models import Product


class CartItem(models.Model):
	"""
	Класс для товаров в корзине, хранит данные о том
	какой товар в корзине и его количество
	"""

	cart_id = models.CharField(max_length=50)
	date_added = models.DateTimeField(auto_now_add=True)
	quantity = models.IntegerField(default=1)
	product = models.ForeignKey(Product, unique=False)

	class Meta:
		db_table = 'cart_items'
		ordering = ['date_added']

	@property
	def total(self):
		"""Метод для подсчета суммы, цена товара * кол-во"""
		return decimal.Decimal(self.quantity * float(self.product.price))

	@property
	def name(self):
		"""Получение названия товара в корзине"""
		return self.product.name

	@property
	def price(self):
		"""Получение цены товара в корзине"""
		return self.product.price

	def get_absolute_url(self):
		"""Получение абсолютной ссылки на товар"""
		return self.product.get_absolute_url()

	def augment_quantity(self, quantity):
		"""Изменение количества товара в корзине"""
		if quantity.isdigit():
			self.quantity = self.quantity + int(quantity)
			self.save()
