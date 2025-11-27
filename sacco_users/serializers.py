from rest_framework import serializers
from .models import SaccoUser

class SaccoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaccoUser
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 'email', 'phone', 'id_number',
            'membership_number', 'county', 'sub_county', 'ward', 'stage',
            'next_of_kin_first_name', 'next_of_kin_last_name', 'next_of_kin_id_number', 'next_of_kin_phone',
            'stage_chairman_first_name', 'stage_chairman_last_name', 'stage_chairman_phone',
            'ward_chairman_first_name', 'ward_chairman_last_name', 'ward_chairman_phone',
            'sub_county_chairman_first_name', 'sub_county_chairman_last_name', 'sub_county_chairman_phone',
            'motor_bike_model', 'motor_bike_registration_number', 'motor_bike_color',
            'qr_code_url'
        ]
        read_only_fields = ['id', 'qr_code_url']

class SaccoUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = SaccoUser
        fields = [
            'first_name', 'middle_name', 'last_name', 'email', 'phone', 'id_number',
            'membership_number', 'county', 'sub_county', 'ward', 'stage',
            'next_of_kin_first_name', 'next_of_kin_last_name', 'next_of_kin_id_number', 'next_of_kin_phone',
            'stage_chairman_first_name', 'stage_chairman_last_name', 'stage_chairman_phone',
            'ward_chairman_first_name', 'ward_chairman_last_name', 'ward_chairman_phone',
            'sub_county_chairman_first_name', 'sub_county_chairman_last_name', 'sub_county_chairman_phone',
            'motor_bike_model', 'motor_bike_registration_number', 'motor_bike_color',
            'password'
        ]

    def create(self, validated_data):
        user = SaccoUser.objects.create_user(**validated_data)
        user.generate_qr_code()
        user.save()
        return user
