from rest_framework.test import APITestCase
from rest_framework import status
from tests.factories.user_factories import UserFactory
from django.contrib.auth import get_user_model
User = get_user_model()

class UserTestCase(APITestCase):

    factory = UserFactory()
    url_users = "/api/v1.0/users/"

    def login_user(self):

        password = "test1234"
        username = "test"
        email = "test@example.com"

        self.user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name="firsttest",
            last_name="lasttest",
            birthdate="1990-10-12",
            age=25,
            phone="+56 9 3435 4354",
            gender="male"
        )

        login_json = {
            "username": username,
            "password": password
        }

        response = self.client.post("/api/v1.0/auth/login", login_json, format="json")
        self.token_access = response.data.get("access")
        self.token_refresh = response.data.get("refresh")

        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.token_access)

    def create_users(self):

        for i in range(1, 6):
            user = self.factory.create_user()

            if i == 1:
                user.gender = "male"
                user.save()

    def test_create_user(self):

        user = self.factory.build_user_JSON()
        response = self.client.post(self.url_users + "register", user, format="json")
        response_user = response.data.get("data")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_user.get("username"), user.get("username"))
        self.assertEqual(User.objects.all().count(), 1)

    def test_fail_user(self):

        user = self.factory.fail_user_JSON()
        response = self.client.post(self.url_users + "register", user, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("errors"))

    def test_get_users(self):

        self.create_users()

        response = self.client.get(self.url_users, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("total_items"), 5)
        self.assertEqual(response.data.get("current_page"), 1)
        self.assertIsNotNone(response.data.get("results"))

    def test_get_limit_skip_users(self):

        self.create_users()

        response = self.client.get(self.url_users + "?limit=2&skip=2", format="json")
        response_user = response.data.get("results")[0]
        list_users = list(User.objects.all()[2:4].values())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("total_items"), 2)
        self.assertCountEqual(response_user.get("username"), list_users[0].get("username"))

    def test_fail_limit_skip_users(self):

        response = self.client.get(self.url_users + "?limit=fsdhfjksd&skip=2", format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("message"))

    def test_search_user(self):

        list_users = []

        for i in range(1, 6):

            user = self.factory.create_user()

            if i == 1:
                list_users.append(user.username)
                list_users.append(user.email)

        response = self.client.get(self.url_users + f"search?username={list_users[0]}")
        response_user_search = response.data.get("results")[0]
        user_filter = User.objects.filter(username__icontains=list_users[0]).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user_search.get("username"), user_filter.username)

        response = self.client.get(self.url_users + f"search?email={list_users[1]}")
        response_user_search = response.data.get("results")[0]
        user_filter = User.objects.filter(email__icontains=list_users[1]).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user_search.get("email"), user_filter.email)

    def test_filter_user(self):

        self.create_users()

        response = self.client.get(self.url_users + "filter?gender=male")
        response_user_filter = response.json().get("results")[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user_filter.get("gender"), "male")

    def test_get_user(self):

        user = self.factory.create_user()

        response = self.client.get(self.url_users + f"user/{user.id}")
        response_user = response.json().get("data")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.get("email"), user.email)

    def test_update_user(self):

        user = self.factory.create_user()

        user_json = {
            "username": "juan7",
            "email": user.email,
            "first_name": "juan",
            "last_name": "perez",
            "birthdate": user.birthdate,
            "age": 25,
            "phone": user.phone,
            "gender": user.gender
        }

        response = self.client.put(self.url_users + f"user/{user.id}", user_json, format="json")
        response_user_update = response.json().get("data")

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertNotEqual(response_user_update.get("username"), user.username)

    def test_delete_user(self):

        user = self.factory.create_user()

        response = self.client.delete(self.url_users + f"user/{user.id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(User.objects.filter(id=user.id).first())

    def test_login_user(self):

        password = "test1234"
        username = "test"
        email = "test@example.com"

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name="firsttest",
            last_name="lasttest",
            birthdate="1990-10-12",
            age=25,
            phone="+56 9 3435 4354",
            gender="male"
        )

        login_json = {
            "username": username,
            "password": password
        }

        response = self.client.post("/api/v1.0/auth/login", login_json, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("refresh"))
    
    def test_logout_user(self):

        self.login_user()
        response = self.client.post("/api/v1.0/auth/logout", {"refresh_token": self.token_refresh}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("message"))

    def test_profile_user(self):

        self.login_user()
        response = self.client.get(self.url_users + "user/me")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), self.user.email)

    def test_refresh_token(self):

        self.login_user()

        response = self.client.post("/api/v1.0/token-jwt/refresh", {"refresh": self.token_refresh}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.token_access, response.data.get("access"))
