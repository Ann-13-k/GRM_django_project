from rest_framework import serializers
from django.utils import timezone
from .models import Sale, ProductSale

class ProductSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSale
        fields = ["product", "quantity"]

class SaleSerializer(serializers.ModelSerializer):
    product_sales = ProductSaleSerializer(many=True, read_only=True)
    class Meta:
        model = Sale
        fields = ["id", "buyer_name", "company", "sale_date", "product_sales"]
        read_only_fields = ["company"]

class SaleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ["buyer_name", "sale_date"]
    def validate_sale_date(self, value):
        now = timezone.now().date()
        if value > now:
            raise serializers.ValidationError("Дата продажи не может быть в будущем")
        return value

class ProductSaleCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

class SaleCreateSerializer(serializers.Serializer):
    buyer_name = serializers.CharField()
    product_sales = ProductSaleCreateSerializer(many=True)