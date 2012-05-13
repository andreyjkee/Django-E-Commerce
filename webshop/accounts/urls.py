# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

from webshop import settings


urlpatterns = patterns('webshop.accounts.views',
	# Форма регистрации
	url(r'^register/$', 'register_view',
		{'template_name': 'registration/register.html' }, # , 'SSL': settings.ENABLE_SSL
		name='register'),
	# Просмотр аккаунта пользователя
	url(r'^my_account/$', 'my_account_view',
		{'template_name': 'registration/my_account.html'},
		name='my_account'),
	# Просмотр информации о сделанном заказе
	url(r'^order_details/(?P<order_id>[-\w]+)/$', 'order_details_view',
		{'template_name': 'registration/order_details.html'},
		name='order_details'),
	# Информация обо всех заказах
	url(r'^orders_info/$', 'order_info_view',
		{'template_name': 'registration/order_info.html'},
		name='order_info'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^login/$', 'login', {'template_name': 'registration/login.html', 'SSL': settings.ENABLE_SSL },
		name='login'),
)
