# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django import template


register = template.Library()

@register.inclusion_tag("tags/form_row.html")
def form_row(form_field):
    """Возвращает вставку для поля типа LineEdit"""
    return {'form_field': form_field }

@register.inclusion_tag("tags/form_choice_field.html")
def choice_field(form_field):
    """Возвращает вставку для поля типа ComboBox"""
    return {'form_field': form_field }
