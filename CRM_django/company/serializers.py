from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("owner",)

class AddEmployeeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        if not attrs.get('user_id') and not attrs.get('email'):
            raise serializers.ValidationError("Передайте user_id или email пользователя")
        return attrs