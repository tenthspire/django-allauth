from rest_framework import serializers
from .models import DomainPuchase, UpdatedDomainDetail

class DomainPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainPuchase
        fields = ['id', 'domain_name', 'contact_info', 'purchse_date', 'status']

class UpdatedDomainDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdatedDomainDetail
        fields = ['domain_name', 'contact_info', 'updated_at']