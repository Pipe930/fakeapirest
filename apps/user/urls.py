from django.urls import path
from .views import RegisterUserView

urls_users = [

    path("register", RegisterUserView.as_view(), name="registeruser")
]
