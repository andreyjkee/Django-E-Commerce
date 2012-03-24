# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from webshop.cart import cart


@csrf_protect
def cart_view(request, template_name="cart/cart.html"):
	"Представление для отображения корзины"
	page_title = _(u'Shopping cart')
	if request.method == 'POST':
		postdata = request.POST.copy()
		if postdata['submit'] == 'Remove':
			cart.remove_from_cart(request)
		if postdata['submit'] == 'Update':
			cart.update_cart(request)
	# Получаем список всех товаров в корзине из cookies
	#cart_item_count = cart.cart_item_count(request)
	cart_items = cart.get_cart_items(request)
	cart_subtotal = cart.cart_subtotal(request)
	return render_to_response(template_name, locals(),
		context_instance=RequestContext(request))
