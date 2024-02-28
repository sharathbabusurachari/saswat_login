# urls.py

from django.urls import path
from .views import SendOTPAPIView, ValidateOTPAPIView, GetGpsView, CustomerTestView, MasterApi

urlpatterns = [
    path('send-otp/', SendOTPAPIView.as_view(), name='send_otp'),
    path('validate-otp/', ValidateOTPAPIView.as_view(), name='validate_otp'),
    path('get-gps/', GetGpsView.as_view(), name='GetGpsView'),
    path('cust-test/', CustomerTestView.as_view(), name='CustomerTestView'),
    path('get-master/', MasterApi.as_view(), name='MasterApi'),
    # Add other URLs as needed
]
