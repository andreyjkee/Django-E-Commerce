# -*- coding: utf-8 -*-
#!/usr/bin/env python
import datetime
import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Order


# Список типов кредитных карт
CARD_TYPES = (('Mastercard', 'Mastercard'),
              ('VISA', 'VISA'),
              ('Maestro', 'Maestro'),
              ('Other', 'Other'),)

def cc_expire_years():
    """Возвращает список возможных годов действия кредитной карты"""
    current_year = datetime.datetime.now().year
    years = range(current_year, current_year+12)
    return [(str(x),str(x)) for x in years]

def cc_expire_months():
    """Возвращает список возможных месяцев действия кредитной карты"""
    months = []
    for month in range(1,13):
        if len(str(month)) == 1:
            numeric = '0' + str(month)
        else:
            numeric = str(month)
        # добавляем в список названия месяцев
        months.append((numeric, datetime.date(2010, month, 1).strftime('%B')))
    return months

def strip_non_numbers(data):
    """Удаляет все символы которые не являются числом
    >>> strip_non_numbers('988f2ds2')
    '98822'
    """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)

# Проверка чтобы тестовые кредитные карты не проходили проверку
def cardLuhnChecksumIsValid(card_number):
    """
    Делаем проверку по алгоритму Луна
    Алгоритм вычисления контрольной цифры номера пластиковых карт
    """
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1 # 0 если четное, 1 если нечетное
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not ((count & 1 ) ^ oddeven):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    return ((sum % 10) == 0)


class CheckoutForm(forms.ModelForm):
    """Форма оформления заказа"""
    credit_card_number = forms.CharField()
    credit_card_type = forms.CharField(widget=forms.Select(choices=CARD_TYPES))
    credit_card_expire_month = forms.CharField(widget=forms.Select(choices=cc_expire_months()))
    credit_card_expire_year = forms.CharField(widget=forms.Select(choices=cc_expire_years()))
    credit_card_cvv = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        # переопределяем аттрибуты по умолчанию
        for field in self.fields:
            self.fields[field].widget.attrs['size'] = '30'
        self.fields['shipping_state'].widget.attrs['size'] = '3'
        self.fields['shipping_zip'].widget.attrs['size'] = '6'
        self.fields['billing_state'].widget.attrs['size'] = '3'
        self.fields['billing_zip'].widget.attrs['size'] = '6'
        self.fields['credit_card_type'].widget.attrs['size'] = '1'
        self.fields['credit_card_expire_year'].widget.attrs['size'] = '1'
        self.fields['credit_card_expire_month'].widget.attrs['size'] = '1'
        self.fields['credit_card_cvv'].widget.attrs['size'] = '5'

    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user', 'transaction_id',)


    def clean_credit_card_number(self):
        """Проверка кредитной карты"""
        cc_number = self.cleaned_data['credit_card_number']
        stripped_cc_number = strip_non_numbers(cc_number)
        if not cardLuhnChecksumIsValid(stripped_cc_number):
            raise forms.ValidationError(_(u'The credit card you entered is invalid.'))

    def clean_phone(self):
        """Проверка телефонного номера (>10 цифр)"""
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 11:
            raise forms.ValidationError(_(u"""
            Enter a valid phone number with area code.(e.g.8-920-351-21-21)"""))
        return self.cleaned_data['phone']
