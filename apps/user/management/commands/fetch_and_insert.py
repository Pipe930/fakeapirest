import requests
import random
from itertools import islice
from django.core.management.base import BaseCommand
from apps.address.models import Region, Address
from apps.product.models import Category, Product, Review
from apps.cart.models import Cart, Item
from apps.post.models import Post, Tags, Comment
from django.contrib.auth import get_user_model
from django.db.models import Model

User = get_user_model()

def get_random_tag(slug: str):

    return Tags.objects.filter(slug=slug).first()

def get_post(id_post: int):

    return Post.objects.filter(id_post=id_post).first()

def get_user(id: int):

    user = User.objects.filter(id=id).first()

    if user is None:

        user_id_random = random.randint(1,200)
        user = User.objects.filter(id=user_id_random).first()

    return user

def get_random_user(users, selected_users):

    if not users:
        raise ValueError("No more users available for selection")

    random_user = random.choice(users)
    selected_users.add(random_user.id)
    users.remove(random_user)

    return random_user


def get_category(name_category: str):
    return Category.objects.filter(slug__icontains=name_category).first()


def get_random_sold():
    return random.randint(1, 100)


def bulk_create_objects(objects_model: tuple, objects_list: list, model: Model):
    while True:
        object_list = list(islice(objects_model, len(objects_list)))

        if not object_list:
            break

        model.objects.bulk_create(object_list)


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
        self.insert_cart()
        self.insert_tag()
        self.insert_post()
        self.insert_comments()

    def request_dummy(self, url: str):

        data = requests.get(self.domain + url)

        if not data.status_code == 200:
            return []

        return data.json()

    def insert_list_address(self, address_object):

        address = {
            "address": address_object.get("address"),
            "city": address_object.get("city"),
            "postal_code": address_object.get("postalCode")
        }

        self.address_list.append(address)

    def insert_users(self):

        users_list = self.request_dummy("users?limit=200")["users"]

        for user in users_list:
            self.insert_list_address(user.get("address"))

        try:
            objects_user = (User(
                first_name=user.get("firstName"),
                last_name=user.get("lastName"),
                username=user.get("username"),
                email=user.get("email"),
                age=user.get("age"),
                phone=user.get("phone"),
                birthdate=user.get("birthDate"),
                gender=user.get("gender"),
                password=user.get("password")
            ) for user in users_list)

            bulk_create_objects(objects_user, users_list, User)

            self.stdout.write(self.style.SUCCESS("[+] Users imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, users weren't registered correctly"))

    def insert_address(self):

        regions = Region.objects.all()

        if regions.exists():
            selected_users = set()
            users = list(User.objects.exclude(id__in=selected_users))

        try:
            objects_address = (Address(

                address=address.get("address"),
                city=address.get("city"),
                postal_code=address.get("postal_code"),
                region=random.choice(regions),
                user=get_random_user(users, selected_users)
            ) for address in self.address_list)

            bulk_create_objects(objects_address, self.address_list, Address)

            self.stdout.write(self.style.SUCCESS("[+] Addresses imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, addresses weren't registered correctly"))

    def insert_regions(self, url_api: str):

        regions_data = requests.get(url_api, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"})

        if regions_data.status_code == 200:
            region_list = regions_data.json()
        else:
            region_list = []

        try:

            objects_region = (Region(
                name=region.get("nombre"),
                code=region.get("codigo"),
                latitude=region.get("lat"),
                longitude=region.get("lng")
            ) for region in region_list)

            bulk_create_objects(objects_region, region_list, Region)
            self.stdout.write(self.style.SUCCESS("[+] Regions imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, users weren't registered correctly"))

    def insert_reviews(self, list_products: list):

        for product_data in list_products:

            product = Product.objects.filter(id_product=product_data.get("id")).first()

            for review in product_data.get("reviews", []):

                Review.objects.create(
                    comment=review.get("comment"),
                    starts=review.get("rating"),
                    reviewer_name=review.get("reviewerName"),
                    reviewer_email=review.get("reviewerEmail"),
                    product=product
                )

    def insert_products(self):

        products_list = self.request_dummy("products?limit=190")["products"]
        try:
            objects_products = (Product(
                title=product.get("title"),
                price=product.get("price"),
                stock=product.get("stock"),
                discount_percentage=product.get("discountPercentage"),
                sold=get_random_sold(),
                brand=product.get("brand"),
                thumbnail=product.get("thumbnail"),
                availability_status=product.get("availabilityStatus"),
                warranty_information=product.get("warrantyInformation"),
                rating=product.get("rating"),
                description=product.get("description"),
                category=get_category(product.get("category"))
            )for product in products_list)

            bulk_create_objects(objects_products, products_list, Product)
            self.stdout.write(self.style.SUCCESS("[+] Products imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, products weren't registered correctly"))

        try:
            self.insert_reviews(products_list)
            self.stdout.write(self.style.SUCCESS("[+] Reviews imported and registered successfully!"))
        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, reviews weren't registered correctly"))

    def insert_categories(self):

        categories_list = self.request_dummy("products/categories")

        try:
            objects_categories = (Category(
                name=category.get("name"),
                slug=category.get("slug")
            ) for category in categories_list)

            bulk_create_objects(objects_categories, categories_list, Category)
            self.stdout.write(self.style.SUCCESS("[+] Categories imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, categories weren't registered correctly"))

    def insert_cart(self):

        carts_list = self.request_dummy("carts?limit=50")["carts"]

        count = 0
        count_cart = 95

        try:
            for cart in carts_list:

                id_user = cart.get("userId")
                count += 1

                id_user = count if id_user > 200 else id_user
                user = User.objects.filter(id=id_user).first()
                cart_exists = Cart.objects.filter(id_cart_user=user.id).first()

                if cart_exists is not None:
                    user = User.objects.filter(id=count_cart).first()

                    cart_created = Cart.objects.create(
                        id_cart_user=user
                    )
                    count_cart += 1
                else:

                    cart_created = Cart.objects.create(
                        id_cart_user=user
                    )

                for product in cart.get("products"):

                    product_exists = Product.objects.filter(id_product=product.get("id")).first()

                    if product_exists is None:
                        product_exists = Product.objects.filter(id_product=random.randint(1, 190)).first()

                    Item.objects.create(

                        cart=cart_created,
                        product=product_exists,
                        quantity=product.get("quantity"),
                        total=0
                    )

            self.stdout.write(self.style.SUCCESS("[+] Carts imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, carts weren't registered correctly"))
    
    def insert_tag(self):

        tags_list = self.request_dummy("posts/tags")

        try:

            objects_tags = (Tags(
                name=tag.get("name"),
                slug=tag.get("slug"),
                description=""
            ) for tag in tags_list)

            bulk_create_objects(objects_tags, tags_list, Tags)
            self.stdout.write(self.style.SUCCESS("[+] Tags imported and registered successfully!"))

        except Exception:
            self.stdout.write(self.style.ERROR("[-] Error, tags weren't registered correctly"))

    def insert_post(self):

        posts_list = self.request_dummy("posts?limit=250")["posts"]

        try:

            objects_posts = (Post(

                title=post.get("title"),
                body=post.get("body"),
                likes=post.get("reactions")["likes"],
                dislikes=post.get("reactions")["dislikes"],
                views=post.get("views"),
                tag=get_random_tag(post.get("tags")[0]),
                author=get_user(post.get("userId"))

            ) for post in posts_list)

            bulk_create_objects(objects_posts, posts_list, Post)
            self.stdout.write(self.style.SUCCESS("[+] Posts imported and registered successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR("[-] Error, posts weren't registered correctly"))
    
    def insert_comments(self):

        comments_list = self.request_dummy("comments?limit=340")["comments"]

        try:

            objects_comments = (Comment(

                body=comment.get("body"),
                likes=comment.get("likes"),
                user=get_user(comment.get("user")["id"]),
                post=get_post(comment.get("postId"))

            ) for comment in comments_list)

            bulk_create_objects(objects_comments, comments_list, Comment)
            self.stdout.write(self.style.SUCCESS("[+] Comments imported and registered successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR("[-] Error, comments weren't registered correctly"))

