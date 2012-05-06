# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from webshop.catalog.forms import ProductAdminForm
from webshop.catalog.models import Product, Category, Characteristic, CharacteristicType


class CharacteristicAdmin(admin.StackedInline):
    model = Characteristic
    extra = 1
    fieldsets = [
        (_(u'Characteristic'), {'fields': ['characteristic_type']}),
        (_(u'Value'), {'fields': ['value']}),
    ]


class ProductAdmin(admin.ModelAdmin):
    """
    Управление товарами
    Как будут отображаться поля товаров в разделе администрирования
    """
    form = ProductAdminForm
    list_display = ('name', 'price', 'old_price', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']
    inlines = [CharacteristicAdmin, ]
    search_field = ['name', 'description', 'meta_keywords', 'meta_description']
    # exclude = ('created_at', 'updated_at',)
    readonly_fields = ('created_at', 'updated_at',)
    # имя продукта для генерации чистой ссылки
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    """
    Управление категориями
    Как будут отображаться поля категорий в разделе администрирования
    """
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)
    # exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('name',)}

# Регистрирация моделей в админке
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CharacteristicType)
