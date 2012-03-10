# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from webshop.catalog.models import Product

class ProductAdminForm(forms.ModelForm):
	class Meta:
		model = Product

	def clean_price(self):
		if self.cleaned_data['price'] <= 0:
			raise forms.ValidationError('Price must be greater than zero.')
		return self.cleaned_data['price']