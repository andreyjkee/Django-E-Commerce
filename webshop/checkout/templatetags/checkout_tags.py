# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django import template


register = template.Library()

@register.inclusion_tag("tags/form_table_row.html")
def form_table_row(form_field):
    """Возвращает список полей формы в виде таблицы"""
    return {'form_field': form_field }
