# urls.py

from django.urls import path
from .views import SendOTPAPIView, ValidateOTPAPIView

urlpatterns = [
    path('send-otp/', SendOTPAPIView.as_view(), name='send_otp'),
    path('validate-otp/', ValidateOTPAPIView.as_view(), name='validate_otp'),
    # Add other URLs as needed
]
