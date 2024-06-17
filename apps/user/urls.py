from django.urls import path
from .views import RegisterUserView, ListUsersView, UserInfoView

urls_users = [

    path("register", RegisterUserView.as_view(), name="registeruser"),
    path("", ListUsersView.as_view(), name="listusers"),
    path("user/me", UserInfoView.as_view(), name="userinfo")
]
