from django.urls import path
from .views import ListCartView, DetailCartView

urls_carts = [

    path("", ListCartView.as_view(), name="listcarts"),
    path("cart/<int:id>", DetailCartView.as_view(), name="")
]