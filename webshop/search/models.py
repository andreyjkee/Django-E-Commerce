# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from django.contrib.auth.models import User


class SearchTerm(models.Model):
    """Класс для хранения поисковых запросов"""
    query = models.CharField(max_length=50)
    search_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()
    user = models.ForeignKey(User, null=True)

    class Meta:
    	db_table = 'search_terms'
    	ordering = ['query']

    def __unicode__(self):
        return self.query
