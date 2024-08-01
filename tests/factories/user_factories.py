from faker import Faker
import random
from django.contrib.auth import get_user_model
User = get_user_model()

class UserFactory:

    faker = Faker()

    def build_user_JSON(self):

        gender_choices = ["male", "female", "other"]
        password = self.faker.password(length=8, digits=True)

        return {
            "username": self.faker.user_name(),
            "email": self.faker.email(domain="example.com"),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "birthdate": self.faker.date_of_birth(minimum_age=18, maximum_age=60),
            "age": 20,
            "phone": self.faker.phone_number(),
            "gender": random.choice(gender_choices),
            "password": password,
            "re_password": password
        }
    
    def fail_user_JSON(self):

        return {
            "username": self.faker.user_name(),
            "email": self.faker.email(domain="example.com"),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "birthdate": self.faker.date_of_birth(minimum_age=18, maximum_age=60),
            "phone": self.faker.phone_number(),
            "gender": "male"
        }
    
    def create_user(self):
        return User.objects.create_user(**self.build_user_JSON())
