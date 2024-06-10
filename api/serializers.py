from rest_framework import serializers
from auth_with_otp.models import UserModel

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'phone_number', 'is_active']

class VerifyPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    class Meta:
        fields = ['phone_number']

class OtpSerializer(serializers.Serializer):
    otp_value = serializers.CharField(max_length=6)
    class Meta:
        fields = ['opt_value']