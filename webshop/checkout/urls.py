# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

from webshop import settings


urlpatterns = patterns('webshop.checkout.views',
    # Страница заказа
    url(r'^$', 'checkout_view', {'template_name': 'checkout/checkout.html',
        'SSL': settings.ENABLE_SSL }, name='checkout'),
    # Просмотр сделанного заказа
    url(r'^receipt/$', 'receipt_view', {'template_name': 'checkout/receipt.html',
        'SSL': settings.ENABLE_SSL }, name='checkout_receipt'),
)
