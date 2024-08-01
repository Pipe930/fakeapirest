from rest_framework.serializers import ModelSerializer, CharField, ValidationError, Serializer, StringRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from apps.address.models import Address

class RegisterUserSerializer(ModelSerializer):

    re_password = CharField(write_only=True)

    class Meta:

        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "age",
            "phone",
            "birthdate",
            "gender",
            "password",
            "re_password"
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }

    
    def validate(self, attrs):

        if attrs.get("password") != attrs.get("re_password"):
            raise ValidationError({"status_code": 400, "message": "La contraseña y confirmacion de contraseña no coinciden"})
        
        if len(attrs.get("password")) < 8:
            raise ValidationError({"status_code": 400, "message": "La contraseña tiene que tener un largo minimo de 8 caracteres"})
        
        if attrs.get("age") <= 16 or attrs.get("age") >= 90:
            raise ValidationError({"status_code": 400, "message": "La edad tiene que estar en un rango de 18 a 100 años"})

        return attrs

    def create(self, validated_data):

        validated_data.pop('re_password')
        user = User.objects.create_user(**validated_data)

        return user

class AddressUserSerializer(ModelSerializer):

    region = StringRelatedField()

    class Meta:

        model = Address
        fields = (
            "address",
            "city",
            "postal_code",
            "region"
        )

class ListUserSerializer(ModelSerializer):

    address = AddressUserSerializer(many=False)
    class Meta:

        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "age",
            "gender",
            "birthdate",
            "phone",
            "address",
            "last_login",
            "created_date",
            "is_staff",
            "is_superuser"
        )

class UpdateUserSerializer(ModelSerializer):

    class Meta:

        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "age",
            "gender",
            "birthdate",
            "phone",
            "is_staff",
            "is_superuser"
        )

    def validate(self, attrs):

        if attrs.get("age") <= 16 or attrs.get("age") >= 90:
            raise ValidationError({"status_code": 400, "message": "La edad tiene que estar en un rango de 18 a 100 años"})

        return attrs
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)
        token["id"] = user.id
        token["username"] = user.username
        token["email"] = user.email
        token["is_superuser"] = user.is_superuser
        token["is_staff"] = user.is_staff

        return token

class LogoutUserSerializer(Serializer):

    refresh_token = CharField()
