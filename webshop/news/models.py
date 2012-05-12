# -*- coding: utf-8 -*-
#!/usr/bin/env python
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    """Класс для хранения новостей"""
    header = models.CharField(_(u'Header'), max_length=255)
    slug = models.SlugField(_(u'Slug'), max_length=255, unique=True)
    body = models.TextField(_(u'Description'))
    created = models.DateTimeField(_(u'Created'), auto_now_add=True)
    updated = models.DateTimeField(_(u'Updated'), null=True)
    user = models.ForeignKey(User, verbose_name=_('User'))
    views = models.IntegerField(_(u'Views count'), blank=True, default=0)

    class Meta:
        db_table = 'news'
        ordering = ['-created']
        get_latest_by = 'created'
        verbose_name = _(u'Post')
        verbose_name_plural = _(u'News')

    def __unicode__(self):
        return self.header

    def was_published_today(self):
        """Проверка опубликовано сегодня или нет"""
        return self.created.date() == datetime.date.today()
    was_published_today.short_description = _(u'Published today?')

    @permalink
    def get_absolute_url(self):
        """Генерация постоянных ссылок на новости"""
        return ('news', (), {'news_slug': self.slug})

