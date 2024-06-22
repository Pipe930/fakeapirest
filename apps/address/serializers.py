from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Address, Region

class CreateRegionSerializer(ModelSerializer):

    class Meta:

        model = Region
        fields = (
            "name",
            "code",
            "latitude",
            "longitude"
        )

class ListAddressSerializer(ModelSerializer):

    region = StringRelatedField()
    user = StringRelatedField()

    class Meta:

        model = Address
        fields = (
            "id_address", 
            "address", 
            "description", 
            "city", 
            "postal_code", 
            "region",
            "user")
        
class CreateAddressSerializer(ModelSerializer):

    class Meta:

        model = Address
        fields = (
            "address", 
            "description", 
            "city", 
            "postal_code", 
            "region",
            "user")

class UpdateAddressSerializer(ModelSerializer):

    class Meta:

        model = Address
        fields = (
            "address", 
            "description", 
            "city", 
            "postal_code", 
            "region")
