from rest_framework.response import Response
from fakeapirest.pagination_custom import CustomPagination
from rest_framework.filters import OrderingFilter
from django.core.exceptions import FieldError
from rest_framework.exceptions import ValidationError as MessageError
from .serializers import ListCategorySerializer, ListProductSerializer, CreateProductSerializer
from django.http import Http404
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

        limit = self.request.query_params.get('limit')
        sort_by = self.request.query_params.get('sortBy')
        order = self.request.query_params.get('order')

        if sort_by and order:
            
            if order == 'desc':
                sort_by = '-' + sort_by
            try:
                self.queryset = self.queryset.order_by(sort_by)
            except FieldError:
                raise MessageError({"status_code": 404, "message": "La columna que ingresaste no existe"}, status.HTTP_404_NOT_FOUND)

        if limit:

            try:
                self.queryset = self.queryset[:int(limit)]
            except ValueError:
                raise MessageError({"status_code": 400, "message": "El limite tiene que ser de tipo numerico"}, status.HTTP_400_BAD_REQUEST)

        return self.queryset

    def get(self, request, format=None):

        users = self.get_queryset()
        pagination = self.paginate_queryset(users)
        serializer = ListProductSerializer(pagination, many=True)

        if not users.exists():

            return Response(
                message_response_no_content("Usuarios"),
                status.HTTP_204_NO_CONTENT
            )
        
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
