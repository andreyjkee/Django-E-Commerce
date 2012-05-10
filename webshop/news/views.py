# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from models import News

from django.shortcuts import get_object_or_404


def news_view(request, news_slug, template_name="news.html"):
    """Представление для конкретной новости"""
    news = get_object_or_404(News, slug=news_slug)
    return render_to_response(template_name,
            {'news': news,}, context_instance=RequestContext(request))

def news_all_view(request, template_name="news_all.html"):
    """Представление для конкретной новости"""
    news = News.objects.all()
    return render_to_response(template_name,
            {'news': news}, context_instance=RequestContext(request))

