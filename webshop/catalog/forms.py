# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Product


class ProductAdminForm(forms.ModelForm):
	"""Форма для управления товаром"""
	class Meta:
		model = Product

	def clean_price(self):
		"""Проверка поля цена"""
		if self.cleaned_data['price'] <= 0:
			raise forms.ValidationError(_(u'Price must be greater than zero.'))
		return self.cleaned_data['price']
