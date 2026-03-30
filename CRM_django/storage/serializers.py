from rest_framework import serializers
from .models import Storage

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ["id", "company", "address"]
        read_only_fields = ["company"]