from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Category, Product, Review

class ListCategorySerializer(ModelSerializer):

    class Meta:

        model = Category
        fields = (
            "id_category",
            "name",
            "slug"
        )

class ListProductSerializer(ModelSerializer):

    category = StringRelatedField()

    class Meta:

        model = Product
        fields = (
            "id_product",
            "title",
            "price",
            "stock",
            "sold",
            "brand",
            "slug",
            "thumbnail",
            "availability_status",
            "warranty_information",
            "review_count",
            "rating",
            "description",
            "create_date",
            "category"
        )

class CreateProductSerializer(ModelSerializer):

    class Meta:

        model = Product
        fields = (
            "title",
            "price",
            "stock",
            "sold",
            "brand",
            "thumbnail",
            "availability_status",
            "warranty_information",
            "rating",
            "description",
            "category"
        )
