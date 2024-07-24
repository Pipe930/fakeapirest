from django.core.exceptions import FieldError
from django.http import Http404
from django.db.models import Q
from rest_framework.response import Response
from fakeapirest.pagination_custom import CustomPagination
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import ValidationError as MessageError
from .serializers import ListCategorySerializer, ListProductSerializer, CreateProductSerializer
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Category, Product
from fakeapirest.message_response import (
    message_response_created,
    message_response_bad_request,
    message_response_no_content,
    message_response_detail,
    message_response_update,
    message_response_delete,
    message_response_list
)

class ListCategoriesView(ListAPIView):

    queryset = Category.objects.all()
    serializer_class = ListCategorySerializer

    def get(self, request, format=None):

        query = self.get_queryset()
        serializer = self.get_serializer(query, many=True)

        if not query.exists():

            return Response(message_response_no_content("categorias"), status.HTTP_204_NO_CONTENT)

        return Response(message_response_list(serializer.data, query.count(), "categorias"), status.HTTP_200_OK)

class ArrayCategoriesView(ListAPIView):

    queryset = Category.objects.all().order_by("name").values("slug")

    def get(self, request, format=None):

        list_categories = []
        query = self.get_queryset()

        if not query.exists():
            return Response(message_response_no_content("categories"), status.HTTP_204_NO_CONTENT)

        for category in query:
            list_categories.append(category.get("slug"))

        return Response(list_categories, status.HTTP_200_OK)

class ListCreateProductView(ListCreateAPIView):

    queryset = Product.objects.all().order_by("title")
    pagination_class = CustomPagination
    limit_queryset = True
    filter_backends = (OrderingFilter,)
    ordering_fields = ("id_product", "title")
    ordering = ("title",)

    def get_queryset(self):

        queryset = self.queryset
        limit = self.request.query_params.get('limit')
        skip = self.request.query_params.get('skip')
        sort_by = self.request.query_params.get('sortBy')
        order = self.request.query_params.get('order')

        if sort_by and order:

            if order == 'desc':
                sort_by = '-' + sort_by
            try:
                queryset = self.queryset.order_by(sort_by)
            except FieldError:
                raise MessageError({"status_code": 404, "message": "La columna que ingresaste no existe"}, status.HTTP_404_NOT_FOUND)

        try:

            skip = 0 if skip is None else int(skip)

            if limit is not None:
                queryset = queryset[:skip + int(limit)]

            if skip is not None:
                queryset = queryset[int(skip):]

        except ValueError:
            raise MessageError({"status_code": 400, "message": "El limite o el skip tiene que ser de tipo numerico"},
                                status.HTTP_400_BAD_REQUEST)

        return queryset

    def get(self, request, format=None):

        users = self.get_queryset()

        if not users.exists():

            return Response(
                message_response_no_content("productos"),
                status.HTTP_204_NO_CONTENT
            )

        pagination = self.paginate_queryset(users)
        serializer = ListProductSerializer(pagination, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):

        serializer = CreateProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(message_response_bad_request("producto", serializer.errors, "POST"), status.HTTP_400_BAD_REQUEST)

        return Response(message_response_created("producto", serializer.data), status.HTTP_201_CREATED)

class DetailProductView(RetrieveUpdateDestroyAPIView):

    def get_object(self, id:int):

        try:
            product = Product.objects.get(id_product=id)
        except Product.DoesNotExist:
            raise Http404

        return product

    def get(self, request, id:int, format=None):

        product = self.get_object(id)
        serializer = ListProductSerializer(product)

        return Response(message_response_detail(serializer.data), status.HTTP_200_OK)

    def put(self, request, id:int, format=None):

        product = self.get_object(id)
        serializer = CreateProductSerializer(product, data=request.data)

        if not serializer.is_valid():

            return Response(message_response_bad_request("producto", serializer.errors, "PUT"), status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(message_response_update("producto", serializer.data), status.HTTP_205_RESET_CONTENT)

    def delete(self, request, id:int, format=None):

        product = self.get_object(id)
        product.delete()

        return Response(message_response_delete("producto"), status.HTTP_204_NO_CONTENT)

class ProductSearchView(ListAPIView):

    serializer_class = ListProductSerializer
    pagination_class = CustomPagination

    def get(self, request, format=None):

        title_product = request.query_params.get("title")
        products = Product.objects.filter(Q(title__icontains=title_product))
        page_list = self.paginate_queryset(products)
        serializer = self.get_serializer(page_list, many=True)

        return self.get_paginated_response(serializer.data)

class ProductFilterView(ListAPIView):

    serializer_class = ListProductSerializer
    pagination_class = CustomPagination

    def get_object(self, name_category:str):

        category = Category.objects.filter(name=name_category).first()

        if category is not None:
            return category

        raise Http404

    def get(self, request, category:str, format=None):

        category = self.get_object(category)
        products_filter = Product.objects.filter(category=category.id_category)
        page_list = self.paginate_queryset(products_filter)
        serializer = self.get_serializer(page_list, many=True)

        return self.get_paginated_response(serializer.data)

