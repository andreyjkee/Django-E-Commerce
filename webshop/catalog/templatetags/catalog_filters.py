# -*- coding: utf-8 -*-
#!/usr/bin/env python
import locale

from django import template


register = template.Library()

@register.filter(name='currency')
def currency(value):
	"""
	Фильтр для конвертирования отображаемой в шаблонах валюты
	Модуль locale для конвертирования
	"""
	try:
		locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	except Exception:
		locale.setlocale(locale.LC_ALL, '')
	loc = locale.localeconv()
	return locale.currency(value, loc['currency_symbol'], grouping=True)
