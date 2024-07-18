from typing import Iterable, Sequence
from django.db import models
from uuid import uuid4
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Category(models.Model):

    id_category = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "category"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class CustomManager(models.Manager):

    def bulk_create(self, objs: Iterable, **kwargs):
        for obj in objs:
            pre_save.send(obj.__class__, instance=obj)
        return super().bulk_create(objs, **kwargs)


class Product(models.Model):

    id_product = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    price = models.PositiveIntegerField(default=0)
    discount_percentage = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=60, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    thumbnail = models.URLField()
    availability_status = models.CharField(max_length=60)
    warranty_information = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    objects = CustomManager()

    class Meta:
        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.title


def set_slug(sender, instance, *args, **kwargs):
    if instance.slug:
        return

    id = str(uuid4())
    instance.slug = slugify("{}-{}".format(instance.title, id[:16]))


pre_save.connect(set_slug, sender=Product)


class Review(models.Model):

    id_review = models.BigAutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    starts = models.PositiveSmallIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    reviewer_name = models.CharField(max_length=40)
    reviewer_email = models.EmailField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        db_table = "review"
        verbose_name = "review"
        verbose_name_plural = "reviews"


class ImageProduct(models.Model):

    id_image_product = models.BigAutoField(primary_key=True)
    url = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
