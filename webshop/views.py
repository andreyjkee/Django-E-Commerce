# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _


def file_not_found_404(request):
	"""Представление для страницы которая не найдена"""
	page_title = _(u'Page Not Found')
	return render_to_response('404.html', locals(), 
		context_instance=RequestContext(request))
