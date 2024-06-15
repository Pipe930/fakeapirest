from rest_framework.serializers import ModelSerializer, CharField, ValidationError
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
