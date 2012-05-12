# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms

from webshop.search.models import SearchTerm


class SearchForm(forms.ModelForm):
    """Форма поиска"""
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        default_text = u'Search...'
        self.fields['query'].widget.attrs['value'] = default_text
        self.fields['query'].widget.attrs['onfocus'] = "if (this.value == '" + default_text + "')this.value = ''"
    include = ('query',)

    class Meta:
        model = SearchTerm

