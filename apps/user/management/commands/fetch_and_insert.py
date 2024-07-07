import requests
import random
from itertools import islice
from django.core.management.base import BaseCommand
from apps.address.models import Region, Address
from apps.product.models import Category, Product
from django.contrib.auth import get_user_model
from django.db.models import Model
User = get_user_model()

class Command(BaseCommand):

    help = "Fetch data from another server and insert to my models"
    address_list = []
    domain = "http://dummyjson.com/"

    def handle(self, *args, **options):

        url_api_region = "https://apis.digital.gob.cl/dpa/regiones"

        self.insert_categories()
        self.insert_regions(url_api_region)
        self.insert_users()
        self.insert_address()
        self.insert_products()

    def request_dummyjson(self, url:str):

        data = requests.get(self.domain + url)

        if not data.status_code == 200:
            return []
        
        return data.json()
    
    def bulk_create_objects(self, objects_model:tuple, objects_list:list, model:Model):

        while True:
            object = list(islice(objects_model, len(objects_list)))

            if not object:
                break

            model.objects.bulk_create(object)
    
    def insert_list_address(self, address_object):

        address = {
            "address": address_object.get("address"),
            "city": address_object.get("city"),
            "postal_code": address_object.get("postalCode")
        }

        self.address_list.append(address)

    def insert_users(self):

        users_list = self.request_dummyjson("users?limit=200")["users"]

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

            self.bulk_create_objects(objects_user, users_list, User)

            self.stdout.write(self.style.SUCCESS("[+] Users imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, users weren't registered correctly"))

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

        try:
            objects_address = (Address(

                address = address.get("address"),
                city = address.get("city"),
                postal_code = address.get("postal_code"),
                region = random.choice(regions),
                user = self.get_random_user(users, selected_users)
            ) for address in self.address_list)

            self.bulk_create_objects(objects_address, self.address_list, Address)
            
            self.stdout.write(self.style.SUCCESS("[+] Addresses imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, addresses weren't registered correctly"))

    def insert_regions(self, url_api:str):

        regions_data = requests.get(url_api, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"})

        if regions_data.status_code == 200:
            region_list = regions_data.json()
        else:
            region_list = []

        try:

            objects_region = (Region(
                name = region.get("nombre"),
                code = region.get("codigo"),
                latitude = region.get("lat"),
                longitude = region.get("lng")
            ) for region in region_list)

            self.bulk_create_objects(objects_region, region_list, Region)
            self.stdout.write(self.style.SUCCESS("[+] Regions imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, users weren't registered correctly"))

    def get_category(self, name_category:str):
        return Category.objects.filter(slug__icontains=name_category).first()
    
    def get_random_sold(self):
        return random.randint(1,1000)

    def insert_products(self):

        products_list = self.request_dummyjson("products?limit=150")["products"]
        
        try:
            objects_products = (Product(
                title = product.get("title"),
                price = product.get("price"),
                stock = product.get("stock"),
                discount_price = product.get("discountPercentage"),
                sold = self.get_random_sold(),
                brand = product.get("brand"),
                thumbnail = product.get("thumbnail"),
                availability_status = product.get("availabilityStatus"),
                warranty_information = product.get("warrantyInformation"),
                rating = product.get("rating"),
                description = product.get("description"),
                category = self.get_category(product.get("category"))
            )for product in products_list)

            self.bulk_create_objects(objects_products, products_list, Product)
            self.stdout.write(self.style.SUCCESS("[+] Products imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, products weren't registered correctly"))

    def insert_categories(self):

        categories_list = self.request_dummyjson("products/categories")

        try:
            objects_categories = (Category(
                name=category.get("name"),
                slug=category.get("slug")
            ) for category in categories_list)

            self.bulk_create_objects(objects_categories, categories_list, Category)
            self.stdout.write(self.style.SUCCESS("[+] Categories imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, categories weren't registered correctly"))
