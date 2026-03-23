from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "storage", "purchase_price", "sale_price", "description"]
        read_only_fields = ["quantity"]
