from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ListAddressSerializer, CreateAddressSerializer, UpdateAddressSerializer, CreateRegionSerializer
from .models import Address, Region
from django.http import Http404
from fakeapirest.message_response import (
    message_response_no_content,
    message_response_list,
    message_response_created,
    message_response_bad_request,
    message_response_detail,
    message_response_update,
    message_response_delete
)

# List and Create Address View
class ListCreateAddressView(ListCreateAPIView):

    queryset = Address.objects.all()

    def get(self, request, format=None):

        query = self.get_queryset()
        serializer = ListAddressSerializer(query, many=True)

        if not query.exists():

            return Response(
                message_response_no_content("direcciones"),
                status.HTTP_204_NO_CONTENT
            )

        return Response(
            message_response_list(serializer.data, query.count(), "direcciones"),
            status.HTTP_200_OK
        )
    
    def post(self, request, format=None):

        serializer = CreateAddressSerializer(data=request.data)
        
        if not serializer.is_valid():

            return Response(
                message_response_bad_request("direccion", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return Response(
            message_response_created("direccion", serializer.data),
            status.HTTP_201_CREATED
        )

# Detail, Update and Delete Address View
class DetailAddressView(RetrieveUpdateDestroyAPIView):

    def get_object(self, id:int):

        try:
            address = Address.objects.get(user=id)
        except Address.DoesNotExist:
            raise Http404

        return address
    
    def get(self, request, id:int, format=None):

        address = self.get_object(id)
        serializer = ListAddressSerializer(address)

        return Response(
            message_response_detail(serializer.data),
            status.HTTP_200_OK
        )
    
    def put(self, request, id:int, format=None):

        address = self.get_object(id)
        serializer = UpdateAddressSerializer(address, data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("direccion", serializer.errors, "PUT"),
                status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return Response(
            message_response_update("direccion", serializer.data),
            status.HTTP_205_RESET_CONTENT
        )
    
    def delete(self, request, id:int, format=None):

        address = self.get_object(id)
        address.delete()

        return Response(
            message_response_delete("direccion"),
            status.HTTP_204_NO_CONTENT
        )

class ListCreateRegionView(ListCreateAPIView):

    queryset = Region.objects.all()
    serializer_class = CreateRegionSerializer

    def get(self, request, format=None):

        query = self.get_queryset()
        serializer = self.get_serializer(query, many=True)

        if not query.exists():

            return Response(
                message_response_no_content("regiones"),
                status.HTTP_204_NO_CONTENT
            )

        return Response(
            message_response_list(serializer.data, query.count(), "regiones"),
            status.HTTP_200_OK
        )
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response(message_response_bad_request("region", serializer.errors, "POST"), status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(message_response_created("region", serializer.data), status.HTTP_201_CREATED)
    