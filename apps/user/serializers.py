from rest_framework.serializers import ModelSerializer, CharField, ValidationError, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from .models import User

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
            raise ValidationError({"message": "La contraseña y confirmacion de contraseña no coinciden"})
        
        if len(attrs.get("password")) < 8:
            raise ValidationError({"message": "La contraseña tiene que tener un largo minimo de 8 caracteres"})

        return attrs

    def create(self, validated_data):

        validated_data.pop('re_password')
        user = User.objects.create_user(**validated_data)

        return user
    
class ListUserSerializer(ModelSerializer):

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
            "last_login",
            "created_date",
            "is_staff",
            "is_superuser"
        )

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
