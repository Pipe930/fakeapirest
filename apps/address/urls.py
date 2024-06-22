from django.urls import path
from .views import ListCreateAddressView, DetailAddressView, ListCreateRegionView


urls_address = [

    path("", ListCreateAddressView.as_view(), name="listcreateaddress"),
    path("address/<int:id>", DetailAddressView.as_view(), name="detailupdatedeleteaddress"),
    path("regions", ListCreateRegionView.as_view(), name="listcreateregion")
]
