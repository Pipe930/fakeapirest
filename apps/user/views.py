from .serializers import RegisterUserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from fakeapirest.message_response import (
    message_response_created,
    message_response_bad_request
)

# Register User View
class RegisterUserView(CreateAPIView):

    serializer_class = RegisterUserSerializer

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("Usuario", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(
            message_response_created("Usuario", serializer.data), 
            status.HTTP_200_OK)
