from rest_framework import serializers
from .models import Supply, SupplyProduct

class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ["id", "supplier", "storage", "delivery_date", "products"]

class SupplyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyProduct
        fields = ["id", "supply", "product", "quantity"]

class SupplyProductCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class SupplyCreateSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    storage_id = serializers.IntegerField()
    products = SupplyProductCreateSerializer(many=True)