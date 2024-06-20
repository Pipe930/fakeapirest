from django.urls import path
from .views import RegisterUserView, ListUsersView, UserInfoView, SearchUsersView, DetailUserView, FilterUserView

urls_users = [

    path("register", RegisterUserView.as_view(), name="registeruser"),
    path("", ListUsersView.as_view(), name="listusers"),
    path("user/me", UserInfoView.as_view(), name="userinfo"),
    path("search", SearchUsersView.as_view(), name="searchusers"),
    path("user/<int:id>", DetailUserView.as_view(), name="detailupdatedeleteuser"),
    path("filter", FilterUserView.as_view(), name="firteruser")
]
