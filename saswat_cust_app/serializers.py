# serializers.py
from rest_framework import serializers
from .models import OTP, UserOtp, GpsModel


# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = ('phone_number', 'otp_code')
#


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOtp
        fields = ('mobile_no', 'otp_code', 'otp_genration_time')

class GpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpsModel
        fields = '__all__'

