from django.contrib.auth import login, authenticate, logout
from django.http import Http404
from .serializers import (
    RegisterUserSerializer,
    ListUserSerializer,
    CustomTokenObtainPairSerializer,
    LogoutUserSerializer,
    UpdateUserSerializer
)
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as MessageError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.core.exceptions import FieldError, ValidationError
from django.db.models import Q
from .models import User
from datetime import date
from fakeapirest.pagination_custom import CustomPagination
from fakeapirest.message_response import (
    message_response_created,
    message_response_bad_request,
    message_response_no_content,
    message_response_detail,
    message_response_update,
    message_response_delete
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

        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "refresh": str(token),
            "access": str(token.access_token),
            "status_code": 200,
            "message": "Authenticacion realizada con exito"
        }, status.HTTP_200_OK)


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


# User Info View
class UserInfoView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ListUserSerializer

    def get_object(self, id: int):

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

        return user

    def get(self, request, format=None):

        user = self.get_object(request.user.id)
        serializer = self.get_serializer(user)

        return Response({
            "first_name": serializer.data["first_name"],
            "last_name": serializer.data["last_name"],
            "username": serializer.data["username"],
            "email": serializer.data["email"],
            "gender": serializer.data["gender"],
            "phone": serializer.data["phone"],
            "age": serializer.data["age"],
            "birthdate": serializer.data["birthdate"],
            "status_code": 200
        })

# List Users View
class ListUsersView(ListAPIView):

    serializer_class = ListUserSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination
    limit_queryset = True
    filter_backends = (OrderingFilter,)
    ordering_fields = ("id", "first_name", "last_name", "username", "email")
    ordering = ("id",)

    def get_queryset(self):

        queryset = self.queryset
        skip = self.request.query_params.get('skip')
        limit = self.request.query_params.get('limit')
        sort_by = self.request.query_params.get('sortBy')
        order = self.request.query_params.get('order')

        if sort_by and order:
            if order == 'desc':
                sort_by = '-' + sort_by
            try:
                queryset = self.queryset.order_by(sort_by)
            except FieldError:
                raise MessageError({"status_code": 400, "message": "La columna que ingresaste no existe"},
                                    status.HTTP_400_BAD_REQUEST)

        else:
            queryset = queryset.order_by(*self.ordering)

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
                message_response_no_content("Usuarios"),
                status.HTTP_204_NO_CONTENT
            )

        pagination = self.paginate_queryset(users)
        serializer = self.get_serializer(pagination, many=True)

        return self.get_paginated_response(serializer.data)


# Search Users View
class SearchUsersView(ListAPIView):

    serializer_class = ListUserSerializer
    pagination_class = CustomPagination

    def get(self, request, format=None):

        username = request.query_params.get('username', None)
        email = request.query_params.get('email', None)
        first_name = request.query_params.get('first_name', None)
        last_name = request.query_params.get('last_name', None)

        filters = Q()
        if username is not None:
            filters &= Q(username__icontains=username)
        if email is not None:
            filters &= Q(email__icontains=email)
        if first_name is not None:
            filters &= Q(first_name__icontains=first_name)
        if last_name is not None:
            filters &= Q(last_name__icontains=last_name)

        users = User.objects.filter(filters)

        if not users.exists():
            return Response({"status": 204, "message": "Usuario no encontrado"}, status.HTTP_204_NO_CONTENT)

        result_page = self.paginate_queryset(users)
        serializer = self.get_serializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


# Filter User View
class FilterUserView(ListAPIView):

    queryset = User.objects.all()
    serializer_class = ListUserSerializer

    def get_queryset(self):

        gender = self.request.query_params.get("gender")
        min_age = self.request.query_params.get("min_age")
        max_age = self.request.query_params.get("max_age")
        date_of_birth = self.request.query_params.get("birthdate")

        query = Q()

        if gender is not None:
            query &= Q(gender=gender)

        try:
            if min_age is not None:

                today = date.today()
                min_birth_date = today.replace(year=today.year - int(min_age))
                query &= Q(birthdate__lte=min_birth_date)

            if max_age:

                today = date.today()
                max_birth_date = today.replace(year=today.year - int(max_age) - 1)
                query &= Q(birthdate__gte=max_birth_date)

        except ValueError:
            raise MessageError({"status_code": 400, "message": "La edad tiene que ser en formato numerico"})

        if date_of_birth is not None:
            query &= Q(birthdate=date_of_birth)

        try:
            self.queryset = self.queryset.filter(query)
        except ValidationError:
            raise MessageError({"status_code": 400, "message": "El formato de fecha no es el correcto"})

        return self.queryset

    def get(self, request, format=None):

        users = self.get_queryset()
        pagination = self.paginate_queryset(users)
        serializer = self.get_serializer(pagination, many=True)

        if not users.exists():
            return Response(
                message_response_no_content("Usuarios"),
                status.HTTP_204_NO_CONTENT
            )

        return self.get_paginated_response(serializer.data)

# Detail, Update and Delete User View
class DetailUserView(RetrieveUpdateDestroyAPIView):

    def get_object(self, id: int):

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

        return user

    def get(self, request, id: int, format=None):

        user = self.get_object(id)
        serializer = ListUserSerializer(user)

        return Response(message_response_detail(serializer.data), status.HTTP_200_OK)

    def update(self, request, id: int, format=None):

        user = self.get_object(id)
        serializer = UpdateUserSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response(message_response_bad_request("Usuario", serializer.errors, "PUT"),
                            status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(message_response_update("Usuario", serializer.data), status.HTTP_205_RESET_CONTENT)

    def delete(self, request, id: int, format=None):

        user = self.get_object(id)
        user.delete()

        return Response(message_response_delete("Usuario"), status.HTTP_204_NO_CONTENT)
