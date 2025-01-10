# domain_manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("search-domain/", views.search_domain, name="search_domain"),
    path("purchase-domain/", views.purchase_domain, name="purchase_domain"),
]
