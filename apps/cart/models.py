from django.db import models
from apps.product.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Cart(models.Model):

    id_cart_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    total_price = models.PositiveIntegerField(default=0)
    discounted_total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_quantity = models.PositiveIntegerField(default=0)
    total_products = models.PositiveIntegerField(default=0)

    class Meta:

        db_table = "cart"
        verbose_name = "cart"
        verbose_name_plural = "carts"

class Item(models.Model):

    id_item = models.BigAutoField(primary_key=True)
    total = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")

    class Meta:
        db_table = "item"
        verbose_name = "item"
        verbose_name_plural = "items"