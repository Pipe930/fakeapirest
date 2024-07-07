from django.urls import path
from .views import ListCategoriesView, ArrayCategoriesView, ListCreateProductView, DetailProductView

urls_category = [

    path("", ListCategoriesView.as_view(), name="listcategories"),
    path("category-list", ArrayCategoriesView.as_view(), name="arraycategories")
]

urls_product = [
    path("", ListCreateProductView.as_view(), name="listcreateproduct"),
    path("product/<int:id>", DetailProductView.as_view(), name="detailupdatedeleteproduct")
]