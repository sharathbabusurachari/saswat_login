# urls.py

from django.urls import path
from .views import SendOTPAPIView, ValidateOTPAPIView, GetGpsView, CustomerTestView

urlpatterns = [
    path('send-otp/', SendOTPAPIView.as_view(), name='send_otp'),
    path('validate-otp/', ValidateOTPAPIView.as_view(), name='validate_otp'),
    path('get-gps/', GetGpsView.as_view(), name='GetGpsView'),
    path('cust-test/', CustomerTestView.as_view(), name='CustomerTestView'),
    # Add other URLs as needed
]
