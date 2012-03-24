# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from webshop.cart import cart
from webshop.catalog.forms import ProductAddToCartForm

from models import Category, Product


def index_view(request, template_name="catalog/index.html"):
	"Представление главной страницы"
	page_title = _(u'Internet Magazine')
	# Функция locals получает все поля словаря
	return render_to_response(template_name, locals(), 
		context_instance=RequestContext(request))
	
def category_view(request, category_slug, template_name="catalog/category.html"):
	"Представление для просмотра конкретной категории"
	c = get_object_or_404(Category, slug=category_slug)
	products = c.product_set.all()
	page_title = c.name
	meta_keywords = c.meta_keywords
	meta_description = c.meta_description
	return render_to_response(template_name, locals(), 
		context_instance=RequestContext(request))

@csrf_protect
def product_view(request, product_slug, template_name="catalog/product.html"):
	"Представление для просмотра конкретного продукта"
	p = get_object_or_404(Product, slug=product_slug)
	categories = p.categories.filter(is_active=True)
	page_title = p.name
	meta_keywords = p.meta_keywords
	meta_description = p.meta_description
	# Проверка HTTP метода
	if request.method == 'POST':
		# Добавление в корзину, создаем связанную форму
		postdata = request.POST.copy()
		form = ProductAddToCartForm(request, postdata)
		# Проверка что отправляемые данные корректны
		if form.is_valid():
			# Добавляем в корзину и делаем перенаправление на страницу с корзиной
			cart.add_to_cart(request)
			# Если cookies работают, читаем их
			if request.session.test_cookie_worked():
				request.session.delete_test_cookie()
			url = urlresolvers.reverse('show_cart')
			return HttpResponseRedirect(url)
	else:
		# Если запрос GET, создаем не привязанную форму. request передаем в kwarg
		form = ProductAddToCartForm(request=request, label_suffix=':')
	# Присваиваем значению скрытого поля чистое имя продукта
	form.fields['product_slug'].widget.attrs['value'] = product_slug
	# Устанавливаем тестовые cookies при первом GET запросе
	request.session.set_test_cookie()
	return render_to_response(template_name, locals(), 
		context_instance=RequestContext(request))
