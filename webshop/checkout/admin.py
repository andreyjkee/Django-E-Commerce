# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin

from webshop.checkout.models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    """Вывод заказов списком"""
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """Управление заказами"""
    list_display = ('__unicode__', 'date', 'status', 'transaction_id', 'user')
    list_filter = ('status', 'date')
    search_fields = ('email', 'shipping_name', 'billing_name', 'id', 'transaction_id')
    inlines = [OrderItemInline, ]
    fieldsets = (
        ('Basics', {'fields': ('status', 'email', 'phone')}),
        ('Shipping', {'fields': ('shipping_name', 'shipping_address_1',
                                'shipping_address_2', 'shipping_city',
                                'shipping_zip', 'shipping_country')}),
        ('Billing', {'fields':('billing_name', 'billing_address',
                               'billing_city', 'billing_zip', 'billing_country')})
        )

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели
        чтобы запомнить пользователя
        """
        # Сохраняем IP если он не был получен ранее
        # Для демонстрации добавления заказа через админку
        if obj.ip_address is None:
            obj.user = request.user
            obj.ip_address = request.META.get('REMOTE_ADDR')
            obj.save()



admin.site.register(Order, OrderAdmin)
