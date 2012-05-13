# -*- coding: utf-8 -*-
#!/usr/bin/env python
from webshop.accounts.models import UserProfile
from webshop.accounts.forms import UserProfileForm


def retrieve(request):
    """Возвразает экземпляр класса форма профиля пользователя"""
    try:
        profile = request.user.get_profile()
    # если у пользователя не было профиля, то создаем его
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    return profile

def set(request):
    """Заполняем форму данными пользователя"""
    profile = retrieve(request)
    profile_form = UserProfileForm(request.POST, instance=profile)
    profile_form.save()
