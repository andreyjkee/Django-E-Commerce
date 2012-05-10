# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin

from webshop.news.models import News


class NewsAdmin(admin.ModelAdmin):
    """Администрирование новостей"""
    list_display = ('header', 'user', 'created',)
    list_display_links = ('header',)
    list_per_page = 20
    search_fields = ['header', 'body']
    exclude = ('updated', 'user',)
    prepopulated_fields = {'slug': ('header',)}

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели
        чтобы запомнить пользователя
        """
        obj.user = request.user
        obj.save()

# Регистрирация модели в админке
admin.site.register(News, NewsAdmin)
