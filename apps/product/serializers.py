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

class ListReviewSerializer(ModelSerializer):

    class Meta:

        model = Review
        fields = (
            "comment",
            "starts",
            "create_date",
            "reviewer_name",
            "reviewer_email"
        )

class ListProductSerializer(ModelSerializer):

    category = StringRelatedField()
    reviews = ListReviewSerializer(many=True, read_only=True)

    class Meta:

        model = Product
        fields = (
            "id_product",
            "title",
            "price",
            "discount_percentage",
            "stock",
            "sold",
            "brand",
            "slug",
            "thumbnail",
            "availability_status",
            "warranty_information",
            "review_count",
            "rating",
            "reviews",
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
