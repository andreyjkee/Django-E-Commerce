# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url


urlpatterns = patterns('webshop.news.views',
# Главная страница
    url(r'^post/(?P<news_slug>[-\w]+)/$', 'news_view',
           {'template_name':'news/news.html'}, name='news'),
    url(r'^allnews/$', 'news_all_view',
           {'template_name':'news/news_all.html'}, name='news_all'),
    )
