from .models import Cart
from .serializers import ListCartSerializer
from fakeapirest.pagination_custom import CustomPagination
from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import ValidationError as MessageError
from fakeapirest.message_response import (
    message_response_no_content,
    message_response_detail
)
from rest_framework import status


class ListCartView(ListAPIView):

    queryset = Cart.objects.all()
    serializer_class = ListCartSerializer
    pagination_class = CustomPagination

    def get_queryset(self):

        queryset = self.queryset
        skip = self.request.query_params.get('skip')
        limit = self.request.query_params.get('limit')

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

        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(message_response_no_content("carritos"), status.HTTP_204_NO_CONTENT)

        list_page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(list_page, many=True)

        return self.get_paginated_response(serializer.data)

class DetailCartView(RetrieveAPIView):

    serializer_class = ListCartSerializer

    def get_object(self, id:int):

        try:
            cart = Cart.objects.get(id_cart_user=id)
        except Cart.DoesNotExist:
            raise Http404

        return cart


    def get(self, request, id:int, format=None):

        cart = self.get_object(id)
        serializer = self.get_serializer(cart)

        return Response(message_response_detail(serializer.data))
