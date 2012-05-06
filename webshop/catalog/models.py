# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Класс для категорий товаров"""
    name = models.CharField(_(u'Name'), max_length=50, unique=True)
    slug = models.SlugField(_(u'Slug'), max_length=50, unique=True,
                            help_text=_(u'Slug for product url created from name.'))
    # "Чистые" ссылки для продуктов формирующиеся из названия
    description = models.TextField(_(u'Description'))
    is_active = models.BooleanField(_(u'Active'), default=True)
    meta_keywords = models.CharField(_(u'Meta keywords'), max_length=255,
                                     help_text=_(u'Comma-delimited set of SEO keywords for meta tag'))
    # Разделенные запятыми теги для SEO оптимизации
    meta_description = models.CharField(_(u'Meta description'), max_length=255,
                                        help_text=_(u'Content for description meta tags'))
    created_at = models.DateTimeField(_(u'Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Updated at'), auto_now=True)
    parent = TreeForeignKey('self', verbose_name=_(u'Parent category'),
                            related_name='children', blank=True,
                            help_text=_(u'Parent-category for current category'), null=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        """Генерация постоянных ссылок на категории"""
        return ('catalog_category', (), {'category_slug': self.slug})


class ProductManager(models.Manager):
    def get_query_set(self):
        return super(ProductManager, self).get_query_set().filter(is_active=True)

    def get_default_image(self, product):
        return ProductImage.objects.get(product=product, default=True)


class Product(models.Model):
    """Класс для товаров"""
    name = models.CharField(_(u'Name'), max_length=255, unique=True)
    slug = models.SlugField(_(u'Slug'), max_length=255, unique=True,
                            help_text=_(u'Unique value for product page URL, created from name.'))
    brand = models.CharField(_(u'Brand'), max_length=50)
    sku = models.CharField(_(u'SKU'), max_length=50,
                           help_text=_(u'Stock-keeping unit')) # кол-во товара на складе
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2,
                                    blank=True, default=0.00)
    is_active = models.BooleanField(_(u'Active'), default=True)
    is_bestseller = models.BooleanField(_(u'Bestseller'), default=False) # Лучшие продажи
    is_featured = models.BooleanField(_(u'Featured'), default=False) # Отображать на главной
    quantity = models.IntegerField(_(u'Quantity'))
    description = models.TextField(_(u'Description'))
    meta_keywords = models.CharField(_(u'Meta keywords'), max_length=255,
                                     help_text=_(u'Comma-delimited set of SEO keywords for meta tag'))
    meta_description = models.CharField(_(u'Meta description'), max_length=255,
                                        help_text=_(u'Content for description meta tag'))
    created_at = models.DateTimeField(_(u'Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Updated at'), auto_now=True)
    categories = models.ManyToManyField(Category, verbose_name=_(u'Categories'),
                                        help_text=_(u'Categories for product'))
    objects = models.Manager()
    active = ProductManager()
#    default_image = models.ForeignKey(ProductImage, verbose_name=_(u'Image'),
#                                      help_text=_(u'Default image for this product'), blank=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name_plural = _(u'Products')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        """Генерация постоянных ссылок на товары"""
        return ('catalog_product', (), {'product_slug': self.slug})

    @property
    def sale_price(self):
        """
        Метод возвращает старую цену товара
        будет использоваться в шаблонах для отображения
        старой цены под текущей
        """
        if self.old_price > self.price:
            return self.price
        else:
            return None


class ProductImage(models.Model):
    """Изображения продуктов"""
    image = models.FileField(_(u'Image'), upload_to='products/images/',
                             help_text='Product image')
    description = models.CharField(_(u'Description'), max_length=255, blank=True)
    product = models.ForeignKey(Product, verbose_name=_(u'Product'),
                                help_text=_(u'Referenced product'))
    default = models.BooleanField(_(u'Default'), default=False)

    class Meta:
        db_table = 'product_images'

    @property
    def url(self):
        return self.image.url


class CharacteristicType(models.Model):
    """Словарная таблица характеристик продуктов"""
    name = models.CharField(_(u'Name'), max_length=255, unique=True)

    class Meta:
        db_table = 'characteristics_type'
        ordering = ['name']
        verbose_name_plural = _(u'Characteristics Types')
        unique_together = ('name',)

    def __unicode__(self):
        return self.name


class Characteristic(models.Model):
    """Характеристики продуктов"""
    characteristic_type = models.ForeignKey(CharacteristicType)
    value = models.CharField(_(u'Value'), max_length=255)
    product = models.ForeignKey(Product, verbose_name=_(u'Product'),
                                help_text=_(u'Referenced product'))

    class Meta:
        db_table = 'characteristics'
        ordering = ['characteristic_type', 'value']
        verbose_name_plural = _(u'Characteristics')
        # составной ключ, для избежания повторения одинковых характеристик у продукта
        unique_together = ('product', 'characteristic_type',)
