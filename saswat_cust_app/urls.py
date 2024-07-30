# urls.py

from django.urls import path
from .views import (SendOTPAPIView, ValidateOTPAPIView, GetGpsView, CustomerTestView, MasterApi,
                    VleVillageInfoView, BmcBasicInformationView, VleBasicInformationView,
                    VleMobileNumberView, PhotoOfBmcView, VLEBankDetailsView, SkillsAndKnowledgeView,
                    VLEEconomicAndSocialStatusInfoView, VleNearbyMilkCenterContactView, VillageDetailsView,
                    VleBasicVillageInfoView, VleValidateOTPAPIView, VleMobileVerificationView, CheckVLEDataView,
                    GetTargetDataView,
                    privacy_policy,
                    QueryDataView,
                    SignInSignOutView,
                    SoAndTaAttachmentAPIView,
                    ESignView, GetESIgnView
                    )

from saswat_cust_app import views

urlpatterns = [
    path('send-otp/', SendOTPAPIView.as_view(), name='send_otp'),
    path('validate-otp/', ValidateOTPAPIView.as_view(), name='validate_otp'),
    path('get-gps/', GetGpsView.as_view(), name='GetGpsView'),
    path('cust-test/', CustomerTestView.as_view(), name='CustomerTestView'),
    path('get-master/', MasterApi.as_view(), name='MasterApi'),
    path('vle-village-info/', VleVillageInfoView.as_view(), name='VleVillageInfoView'),
    path('vle-basic-village-info/', VleBasicVillageInfoView.as_view(), name='VleBasicVillageInfoView'),
    path('bmc-basic-info/', BmcBasicInformationView.as_view(), name='BmcBasicInformationView'),
    path('vle-basic-info/', VleBasicInformationView.as_view(), name='VleBasicInformationView'),
    path('vle-mobile-number/', VleMobileNumberView.as_view(), name='VleMobileNumberView'),
    path('photo-of-bmc/', PhotoOfBmcView.as_view(), name='PhotoOfBmcView'),
    path('vle-bank-details/', VLEBankDetailsView.as_view(), name='VLEBankDetailsView'),
    path('skills-and-knowledge/', SkillsAndKnowledgeView.as_view(), name='SkillsAndKnowledgeView'),
    path('vle-eco-status/', VLEEconomicAndSocialStatusInfoView.as_view(), name='VLEEconomicAndSocialStatusInfoView'),
    path('near-by-milk-center-cont/', VleNearbyMilkCenterContactView.as_view(), name='VleNearbyMilkCenterContactView'),
    path('village-details/', VillageDetailsView.as_view(), name='VillageDetailsView'),
    path('vle-mo-verification/', VleMobileVerificationView.as_view(), name='VleMobileVerificationView'),
    path('vle-validate-otp/', VleValidateOTPAPIView.as_view(), name='VleValidateOTPAPIView'),
    path('check-vle-data/', CheckVLEDataView.as_view(), name='CheckVLEDataView'),
    path('get-target-data/', GetTargetDataView.as_view(), name='get_target_data'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('query-data/', QueryDataView.as_view(), name='query_data'),
    path('signin-signout/', SignInSignOutView.as_view(), name='signin_sign_out'),
    path('query-attachments/', SoAndTaAttachmentAPIView.as_view(), name='attachment-query-create'),
    path('get_shortened_query_details/<int:pk>/', views.get_shortened_query_details, name='get_shortened_query_details'),
    path('get_documents/<int:document_id>/', views.get_documents, name='get_documents'),
    path('esign/', ESignView.as_view(), name='esign'),
    path('get-esign/', GetESIgnView.as_view(), name='get_esign'),
]
