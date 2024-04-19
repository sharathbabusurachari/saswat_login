# urls.py

from django.urls import path
from .views import (SendOTPAPIView, ValidateOTPAPIView, GetGpsView, CustomerTestView, MasterApi,
                    VleVillageInfoView, BmcBasicInformationView, VleBasicInformationView,
                    VleMobileNumberView, PhotoOfBmcView, VLEBankDetailsView, SkillsAndKnowledgeView,
                    VLEEconomicAndSocialStatusInfoView, VleNearbyMilkCenterContactView, VillageDetailsView)

urlpatterns = [
    path('send-otp/', SendOTPAPIView.as_view(), name='send_otp'),
    path('validate-otp/', ValidateOTPAPIView.as_view(), name='validate_otp'),
    path('get-gps/', GetGpsView.as_view(), name='GetGpsView'),
    path('cust-test/', CustomerTestView.as_view(), name='CustomerTestView'),
    path('get-master/', MasterApi.as_view(), name='MasterApi'),
    path('vle-village-info/', VleVillageInfoView.as_view(), name='VleVillageInfoView'),
    path('bmc-basic-info/', BmcBasicInformationView.as_view(), name='VleVillageInfoView'),
    path('vle-basic-info/', VleBasicInformationView.as_view(), name='VleVillageInfoView'),
    path('vle-mobile-number/', VleMobileNumberView.as_view(), name='VleVillageInfoView'),
    path('photo-of-bmc/', PhotoOfBmcView.as_view(), name='VleVillageInfoView'),
    path('vle-bank-details/', VLEBankDetailsView.as_view(), name='VleVillageInfoView'),
    path('skills-and-knowledge/', SkillsAndKnowledgeView.as_view(), name='VleVillageInfoView'),
    path('vle-eco-status/', VLEEconomicAndSocialStatusInfoView.as_view(), name='VleVillageInfoView'),
    path('near-by-milk-center-cont/', VleNearbyMilkCenterContactView.as_view(), name='VleVillageInfoView'),
    path('village-details/', VillageDetailsView.as_view(), name='VleVillageInfoView'),
]
