from django.contrib.auth import login, authenticate, logout
from django.http import Http404
from .serializers import RegisterUserSerializer, ListUserSerializer, CustomTokenObtainPairSerializer, LogoutUserSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .models import User
from rest_framework import status
from fakeapirest.message_response import (
    message_response_created,
    message_response_bad_request,
    message_response_list,
    message_response_no_content
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
            status.HTTP_201_CREATED)

# Login Authenticate User View
class LoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=request.data["username"], 
            password=request.data["password"])
        
        if user is None:

            return Response(
                {"status_code": 401, "error": "Usuario o contraseña invalidos"},
                status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:

            return Response(
                {"status_code": 401, "error": "El usuario no se encuentra activo"}
            )
        
        login(request, user)
        
        token = self.get_serializer().get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "refresh": refresh_token,
            "access": access_token,
            "status_code": 200,
            "message": "Authenticacion realizada con exito"
        })
    
# Logout User View
class LogoutView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutUserSerializer

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:

            token = RefreshToken(serializer.validated_data["refresh_token"])
            token.blacklist()

            logout(request)
        except TokenError:
            return Response({"status_code": 400, "message": "Este token ya esta en la lista negra"},
                            status.HTTP_400_BAD_REQUEST)

        return Response({"status_code": 200, "message": "Sesion terminada con exito"},
                            status.HTTP_200_OK)

# Refresh Token User View
class TokenRefreshView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TokenRefreshSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response({"status_code": 400, "message": "Token invalido o expirado"})

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class UserInfoView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ListUserSerializer

    def get_object(self, id:int):

        try:
            user = User.objects.get(id=id)

        except User.DoesNotExist:
            raise Http404

        return user
    
    def get(self, request, format=None):

        user = self.get_object(request.user.id)
        serializer = self.get_serializer(user)

        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "gender": user.gender,
            "phone": user.phone,
            "age": user.age,
            "birthdate": user.birthdate,
            "status_code": 200
        })


# List Users View
class ListUsersView(ListAPIView):

    serializer_class = ListUserSerializer
    queryset = User.objects.all().order_by("id")

    def get(self, request, format=None):

        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)

        if not users.exists():

            return Response(
                message_response_no_content("Usuarios"),
                status.HTTP_204_NO_CONTENT
            )

        return Response(
            message_response_list(serializer.data, users.count(), "usuarios"),
            status.HTTP_200_OK)

