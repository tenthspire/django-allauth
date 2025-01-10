from django.urls import path
from . import views

urlpatterns = [
    path('check-domain/', views.check_domain_availability, name='check_domain'),
    path('get-domain-info/', views.get_domain_info, name='get_domain_info'),
]
