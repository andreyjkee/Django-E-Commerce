# -*- coding: utf-8 -*-
#!/usr/bin/env python
from webshop import settings
from webshop.catalog.models import Category

def webshop(request):
	"Обработчки контекстов(словарей) для использования в шаблонах"
	return {
			'active_categories': Category.objects.filter(is_active=True),
			'site_name': settings.SITE_NAME,
			'meta_keywords': settings.META_KEYWORDS,
			'meta_description': settings.META_DESCRIPTION
		}