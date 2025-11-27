from rest_framework import serializers
from .models import SaccoUser

class SaccoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaccoUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'id_number', 'qr_code_url']
        read_only_fields = ['id', 'qr_code_url']

class SaccoUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = SaccoUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'id_number', 'password']

    def create(self, validated_data):
        user = SaccoUser.objects.create_user(**validated_data)
        user.generate_qr_code()
        user.save()
        return user
