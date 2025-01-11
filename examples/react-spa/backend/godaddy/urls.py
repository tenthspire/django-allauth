# domain_manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("search-domain/", views.search_domain, name="search_domain"),
    path("purchase-domain/", views.purchase_domain, name="purchase_domain"),
    path("list-domain-purchases/", views.list_domain_purchases, name="list_domain_purchases"),
    path('update-domain-contact/', views.update_domain_contact, name='update_domain_contact'),
]