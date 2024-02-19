# serializers.py
from rest_framework import serializers
from .models import OTP, UserOtp


# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = ('phone_number', 'otp_code')
#


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOtp
        fields = ('mobile_no', 'otp_code', 'otp_genration_time')


