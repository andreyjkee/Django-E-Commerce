# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from webshop.checkout.forms import CheckoutForm
from webshop.checkout.models import Order, OrderItem
from webshop.checkout import checkout
from webshop.cart import cart


def checkout_view(request, template_name='checkout/checkout.html'):
    """Представление для оформления заказа"""
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            response = checkout.process(request)
            order_number = response.get('order_number', 0)
            error_message = response.get('message', '')
            if order_number:
                request.session['order_number'] = order_number
                receipt_url = urlresolvers.reverse('checkout_receipt')
                return HttpResponseRedirect(receipt_url)
        else:
            error_message = _(u'Correct the errors below')
    else:
        form = CheckoutForm()
    page_title = _(u'Checkout')
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def receipt_view(request, template_name='checkout/receipt.html'):
    """Представление отображающее сделанный заказ"""
    order_number = request.session.get('order_number', '')
    if order_number:
        # если в cookies есть номер заказа, выводим его содержимое
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session['order_number']
    else:
        # иначе перенаправляем пользователя на страницу корзины
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
