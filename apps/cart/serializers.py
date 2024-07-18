from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Cart, Item
from apps.product.models import Product


class ProductCartSerializer(ModelSerializer):

    class Meta:

        model = Product
        fields = (
            "id_product",
            "title",
            "price",
            "discount_percentage"
        )


class ItemsCartSerializer(ModelSerializer):

    product = ProductCartSerializer(many=False)
    total = SerializerMethodField(method_name="calculate_total")

    class Meta:

        model = Item
        fields = (
            "total",
            "quantity",
            "product"
        )

    def calculate_total(self, item: Item):

        result = item.product.price * item.quantity

        item.total = result
        item.save()

        return result


class ListCartSerializer(ModelSerializer):

    items = ItemsCartSerializer(many=True, read_only=True)
    total_price = SerializerMethodField(method_name="calculate_price")
    discounted_total = SerializerMethodField(method_name="calculate_discounted")
    total_quantity = SerializerMethodField(method_name="calculate_quantity")
    total_products = SerializerMethodField(method_name="calculate_products")

    class Meta:

        model = Cart
        fields = (

            "id_cart_user",
            "items",
            "total_price",
            "discounted_total",
            "total_quantity",
            "total_products"
        )

    def get_items(self, cart: Cart):

        return cart.items.all()

    def calculate_price(self, cart: Cart):

        items = self.get_items(cart)

        cart.total_price = sum([item.quantity * item.product.price for item in items])
        cart.save()

        return cart.total_price


    def calculate_quantity(self, cart: Cart):

        items = self.get_items(cart)
        total_quantity = 0

        for item in items:
            total_quantity += item.quantity

        return total_quantity

    def calculate_discounted(self, cart: Cart):

        items = self.get_items(cart)

        discounted_total = 0

        for item in items:

            product_discount_price = item.product.price - round(item.product.price * item.product.discount_percentage / 100, 2)
            discounted_total += product_discount_price * item.quantity

        cart.discounted_total = discounted_total
        cart.save()

        return discounted_total

    def calculate_products(self, cart: Cart):

        return cart.items.count()


