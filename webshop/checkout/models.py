# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _


from webshop.catalog.models import Product


class BaseOrderInfo(models.Model):
    """Абстрактный класс для заказов"""
    class Meta:
        abstract = True

    # Контактная информация
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    # Информация об адресе для отправки товара
    shipping_name = models.CharField(max_length=50)
    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50, blank=True)
    shipping_city = models.CharField(max_length=50)
    #shipping_country = models.CharField(max_length=50) #Область
    shipping_country = models.CharField(max_length=50)
    shipping_zip = models.CharField(max_length=10)
    # Информация о плательщике
    billing_name = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=50)
    billing_city = models.CharField(max_length=50)
    billing_country = models.CharField(max_length=50)
    billing_zip = models.CharField(max_length=10)


class Order(BaseOrderInfo):
    """Класс для заказа"""

    # Константы статуса
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4

    # Словарь возможных статусов заказа
    ORDER_STATUSES = ((SUBMITTED, _(u'Submitted')),
                      (PROCESSED, _(u'Processed')),
                      (SHIPPED, _(u'Shipped')),
                      (CANCELLED, _(u'Cancelled')),)

    # Информация о заказе
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    transaction_id = models.CharField(max_length=20)

    def __unicode__(self):
        return _(u'Order #') + str(self.id)

    @property
    def total(self):
        """Общая сумма заказа"""
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    @permalink
    def get_absolute_url(self):
        """Абсолютная ссылка для просмотра заказа"""
        return ('order_details', (), { 'order_id': self.id })


class OrderItem(models.Model):
    """Конкретный товар в заказе"""
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order)

    @property
    def total(self):
        """Сумма для товара"""
        return self.quantity * self.price

    @property
    def name(self):
        """Название товара"""
        return self.product.name

    @property
    def sku(self):
        """Количество товара на складе"""
        return self.product.sku

    def __unicode__(self):
        return self.product.name + ' (' + self.product.sku + ')'

    def get_absolute_url(self):
        """Абсолютная ссылка на товар в корзине"""
        return self.product.get_absolute_url()
