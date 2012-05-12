# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin

from webshop.search.models import SearchTerm


class SearchTermAdmin(admin.ModelAdmin):
    """Просмотр результатов поиска"""
    list_display = ('__unicode__','ip_address','search_date')
    list_filter = ('ip_address', 'user', 'query')
    exclude = ('user', 'ip_address',)

# Регистрирация моделей в админке
admin.site.register(SearchTerm, SearchTermAdmin)