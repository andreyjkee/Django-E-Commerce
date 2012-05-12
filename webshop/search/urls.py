# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url


urlpatterns = patterns('webshop.search.views',
    # Просмотр корзины
    url(r'^results/$', 'results_view', {'template_name': 'search/results.html'}, name='search_results'),

)
