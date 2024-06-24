import requests
import random
from itertools import islice
from django.core.management.base import BaseCommand
from apps.address.models import Region, Address
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):

    help = "Fetch data from another server and insert to my models"
    address_list = []
    domain = "http://dummyjson.com/"

    def handle(self, *args, **options):

        url_api_region = "https://apis.digital.gob.cl/dpa/regiones"

        self.insert_regions(url_api_region)
        self.insert_users()
        self.insert_address()
    
    def insert_list_address(self, address_object):

        address = {
            "address": address_object.get("address"),
            "city": address_object.get("city"),
            "postal_code": address_object.get("postalCode")
        }

        self.address_list.append(address)

    def insert_users(self):

        users_data = requests.get(self.domain + "users?limit=100")

        if users_data.status_code == 200:
            users_list = users_data.json()["users"]
        else:
            users_list = []

        for user in users_list:

            self.insert_list_address(user.get("address"))

        try:
            objects_user = (User(
                first_name = user.get("firstName"),
                last_name = user.get("lastName"),
                username = user.get("username"),
                email = user.get("email"),
                age = user.get("age"),
                phone = user.get("phone"),
                birthdate = user.get("birthDate"),
                gender = user.get("gender"),
                password = user.get("password")
            ) for user in users_list)

            while True:
                user = list(islice(objects_user, len(users_list)))

                if not user:
                    break

                User.objects.bulk_create(user)

            self.stdout.write(self.style.SUCCESS("Users imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("Error, users weren't registered correctly"))
            


    def get_random_user(self, users, selected_users):

        if not users:
            raise ValueError("No more users available for selection")

        random_user = random.choice(users)
        selected_users.add(random_user.id)
        users.remove(random_user)

        return random_user

    def insert_address(self):

        regions = Region.objects.all()

        if regions.exists():
            selected_users = set()
            users = list(User.objects.exclude(id__in=selected_users))
        
        objects_address = (Address(

            address = address.get("address"),
            city = address.get("city"),
            postal_code = address.get("postal_code"),
            region = random.choice(regions),
            user = self.get_random_user(users, selected_users)
        ) for address in self.address_list)

        while True:
            address = list(islice(objects_address, len(self.address_list)))

            if not address:
                break

            Address.objects.bulk_create(address)
        
        self.stdout.write(self.style.SUCCESS("Addresses imported and registered successfully!"))

    def insert_regions(self, url_api:str):

        regions_data = requests.get(url_api, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"})

        if regions_data.status_code == 200:
            region_list = regions_data.json()
        else:
            region_list = []

        objects_region = (Region(
            name = region.get("nombre"),
            code = region.get("codigo"),
            latitude = region.get("lat"),
            longitude = region.get("lng")
        ) for region in region_list)

        while True:
            region = list(islice(objects_region, len(region_list)))

            if not region:
                break

            Region.objects.bulk_create(region)

        self.stdout.write(self.style.SUCCESS("Regions imported and registered successfully!"))
