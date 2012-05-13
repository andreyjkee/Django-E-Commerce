# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms

from models import UserProfile


class UserProfileForm(forms.ModelForm):
    """Форма для профиля пользователя"""
    class Meta:
        model = UserProfile
        exclude = ('user',)
