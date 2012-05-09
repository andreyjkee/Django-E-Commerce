# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal
import random

from django.shortcuts import get_object_or_404

from webshop.catalog.models import Product
from webshop.cart.models import CartItem


CART_ID_SESSION_KEY = 'cart_id'

def _cart_id(request):
    """
      Получение id корзины из cookies для пользователя,
      или установка новых cookies если не существуют
      _модификатор для видимости в пределах модуля
      """
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]

def _generate_cart_id():
    """Генерация уникального id корзины который будет хранится в cookies"""
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id

def get_cart_items(request):
    """Получение всех товаров для текущей корзины"""
    return CartItem.objects.filter(cart_id=_cart_id(request))

def add_to_cart(request):
    """Добавление товара в корзину"""
    postdata = request.POST.copy()
    # Получаем чистое имя товара, возвращает пустую строку если нет
    product_slug = postdata.get('product_slug', '')
    # Получаем количество добавлеых товаров, возрат 1 если нет
    quantity = postdata.get('quantity', 1)
    # Получаем товар, или возвращаем ошибку "не найден" если его не существует
    p = get_object_or_404(Product, slug=product_slug)
    # Получаем товары в корзине
    cart_products = get_cart_items(request)
    product_in_cart = False
    # Проверяем что продукт уже в корзине
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            # Обновляем количество если найден
            cart_item.augment_quantity(quantity)
            product_in_cart = True
    if not product_in_cart:
        # Создаем и сохраняем новую корзину
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()

def cart_distinct_item_count(request):
    """Возвращает общее количество товаров в корзине"""
    return get_cart_items(request).count()

def get_single_item(request, item_id):
    """Получаем конкретный товар в корзине"""
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))

def update_cart(request):
    """Обновляет количество отдельного товара"""
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
    #else:
    #TODO: добавить предупреждение
    #    remove_from_cart(request)

def remove_from_cart(request):
    """Удаляет выбранный товар из корзины"""
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()

def cart_subtotal(request):
    """Получение суммарной стоимости всех товаров"""
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.product.price * cart_item.quantity
    return cart_total

def is_empty(request):
    """Если корзина пустая возвращаем True"""
    return cart_distinct_item_count(request) == 0

def empty_cart(request):
    """Очищает корзину покупателя"""
    user_cart = get_cart_items(request)
    user_cart.delete()
