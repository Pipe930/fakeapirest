from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Region(models.Model):

    id_region = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)
    latitude = models.DecimalField(max_digits=7, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)

    class Meta:

        db_table = "region"
        verbose_name = "region"
        verbose_name_plural = "regions"

    def __str__(self):
        return self.name

class Address(models.Model):

    id_address = models.BigAutoField(primary_key=True)
    address = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=10)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:

        db_table = "address"
        verbose_name = "address"
        verbose_name_plural = "addresses"
