# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Product


class ProductAdminForm(forms.ModelForm):
	"Форма для управления товаром"
	class Meta:
		model = Product

	def clean_price(self):
		"Проверка поля цена"
		if self.cleaned_data['price'] <= 0:
			raise forms.ValidationError(_(u'Price must be greater than zero.'))
		return self.cleaned_data['price']


class ProductAddToCartForm(forms.Form):
	"Форма добавления товара в корзину"
	quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '2',
		'value': '1', 'class': 'quantity', 'maxlength': '5'}),
		error_messages={'invalid': _(u'Please enter a valid quantity.')},
		min_value=1)
	product_slug = forms.CharField(widget=forms.HiddenInput())

	def __init__(self, request=None, *args, **kwargs):
		"""
		Переопределение метода __init__ по умолчанию для получения словаря request
		нужен для проверки работы cookies
		"""
		self.request = request
		super(ProductAddToCartForm, self).__init__(*args, **kwargs)

	def clean(self):
		"Проверка что cookies в браузере включены"
		if self.request:
			if not self.request.session.test_cookie_worked():
				raise forms.ValidationError(_(u'Cookies must be enabled.'))
		return self.cleaned_data