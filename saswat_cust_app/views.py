# import string
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
# from django.shortcuts import get_object_or_404
# from .utils import is_valid_indian_mobile_number

from saswat_cust_app.models import UserOtp, UserDetails, CustomerTest, Gender, State
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import random
from saswat_cust_app.serializers import (OTPSerializer, GpsSerializer, CustomerTestSerializer,
                                         GenderSerializer, StateSerializer,
                                         VleVillageInfoSerializer, BmcBasicInformationSerializer,
                                         VleBasicInformationSerializer, VleMobileNumberSerializer,
                                         PhotoOfBmcSerializer, VLEBankDetailsSerializer,
                                         SkillsAndKnowledgeSerializer, VLEEconomicAndSocialStatusInfoSerializer,
                                         VleNearbyMilkCenterContactSerializer,
                                         VillageDetailsSerializer)
from datetime import datetime, timedelta
import requests
# from rest_framework.authentication import SessionAuthentication
from .authenticate import MobileNumberAuthentication
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class SendOTPAPIView(APIView):

    def post(self, request, *args, **kwargs):
        mobile_no = request.data.get('mobile_no')
        url = 'http://20.235.255.141:8080/saswat/otp'
        #url = 'http://20.235.246.32:8080/message/telspielmessage'
        try:
            existing_otp = UserOtp.objects.filter(mobile_no=mobile_no).order_by('otp_genration_time').first()
            if existing_otp is not None:
                existing_otp.is_expired()
                existing_otp.delete()
                response_data = {
                    'status': '02',
                    'message': "An OTP has already been sent",

                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # if not is_valid_indian_mobile_number(mobile_no):
            #     return JsonResponse({'error': 'Invalid Indian mobile number format'}, status=400)
            elif UserDetails.objects.filter(mobile_no=mobile_no).exists():
                otp_code = str(random.randint(1000, 9999))
                data = {
                    'otp': otp_code,
                    'dest': mobile_no,
                    'msgName': "OTP"
                }

                response = requests.post(url, json=data)
                print(response)
                if response.status_code == 200:
                    # result = response.json()
                    UserOtp.objects.create(mobile_no=str(mobile_no), otp_code=otp_code)
                    response_data = {
                        'status': '00',
                        'message': "OTP sent successfully",

                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        'status': '01',
                        'message': "Failed to send OTP to the user",

                    }
                    return Response(response_data,
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                response_data = {
                    'status': '01',
                    'message': "Mobile number does not exist",

                }
                return Response(response_data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'message': 'Error occurred while making the request'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidateOTPAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [MobileNumberAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_no = serializer.validated_data['mobile_no']
            otp_code = serializer.validated_data['otp_code']

            if UserDetails.objects.filter(mobile_no=mobile_no).exists():
                check_valid_time = datetime.now() - timedelta(minutes=1)
                user_det = UserDetails.objects.filter(mobile_no=mobile_no).first()
                valid_otp_mobile = UserOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code).first()
                valid_otp_time = UserOtp.objects.filter(mobile_no=mobile_no,
                                                        otp_expiration_time__lt=timezone.now()).first()

                verify_user_otp = UserOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code,
                                                         otp_genration_time__gte=check_valid_time).first()
                session_id = request.auth

                # otp_instance = get_object_or_404(UserOtp, mobile_no=str(mobile_no), otp_code=otp_code)
                if verify_user_otp:
                    # user_info = [{
                    #     'user_id': user_det.user_id,
                    #     "first_name": user_det.first_name,
                    #     "mid_name": user_det.mid_name,
                    #     "last_name": user_det.last_name,
                    #     "work_dept": user_det.work_dept,
                    #     "mobile_no": user_det.mobile_no,
                    #     "designation": user_det.designation,
                    #     "designation_id": user_det.designation_id
                    # }]
                    response_data = {
                        'status': '00',
                        'message': "OTP verified successfully",
                        'session_id': session_id,
                        'user_id': user_det.user_id,
                        "first_name": user_det.first_name,
                        "mid_name": user_det.mid_name,
                        "last_name": user_det.last_name,
                        "work_dept": user_det.work_dept,
                        "mobile_no": user_det.mobile_no,
                        "designation": user_det.designation,
                        "designation_id": user_det.designation_id
                    }
                    verify_user_otp.delete()
                    return Response(response_data, status=200)
                elif valid_otp_time:
                    response_data = {
                        'status': '01',
                        'message': "OTP has expired",
                    }
                    valid_otp_time.delete()
                    return Response(response_data, status=status.HTTP_200_OK)
                elif valid_otp_mobile:
                    valid_otp_mobile.delete()
                else:
                    response_data = {
                        'status': '01',
                        'message': "Invalid OTP",
                    }
                    return JsonResponse(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'status': '01',
                    'message': "Mobile number does not exist",
                }
                return JsonResponse(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetGpsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        get_gps_serializer = GpsSerializer(data=request.data)
        try:
            if get_gps_serializer.is_valid():
                get_gps_serializer.save()
                response_data = {
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(get_gps_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CustomerTestView(ListCreateAPIView):
#     co_applicant_det = CustomerTest.objects.all()
#     serializer_class = CustomerTestSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
#         serializer.is_valid(raise_exception=True)
#         try:
#             self.perform_create(serializer)
#         except Exception as e:
#             # Handle any errors that occur during creation
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save()

class CustomerTestView(ListCreateAPIView):
    co_applicant_det = CustomerTest.objects.all()
    serializer_class = CustomerTestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        try:
            serializer.is_valid(raise_exception=True)
            # self.perform_create(serializer)
        except ValidationError as e:
            if 'c_id' in e.detail:
                response_data = {
                    'status': '01',
                    'message': "Customer   already exist",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
            'status': '00',
            'message': "success",
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()

class MasterApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            master_gender = Gender.objects.all()
            master_state = State.objects.all()
            gender_data = GenderSerializer(master_gender, many=True)
            state_data = StateSerializer(master_state, many=True)
            response_data = {
                'status': '00',
                'message': "success",
                'gender_data': gender_data.data,
                'state_data': state_data.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VleVillageInfoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        vle_v_info_serializer = VleVillageInfoSerializer(data=request.data)
        print(vle_v_info_serializer)
        try:
            if vle_v_info_serializer.is_valid():
                vle_id_instance = vle_v_info_serializer.save()
                print(vle_id_instance)
                response_data = {
                    'Vle id': vle_id_instance.vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_v_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BmcBasicInformationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        bmc_basic_info_serializer = BmcBasicInformationSerializer(data=request.data)
        try:
            if bmc_basic_info_serializer.is_valid():
                vle_id_instance = bmc_basic_info_serializer.save()
                serialized_data = BmcBasicInformationSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')

                response_data = {
                    'Vle id': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(bmc_basic_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleBasicInformationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        vle_basic_info_serializer = VleBasicInformationSerializer(data=request.data)
        try:
            if vle_basic_info_serializer.is_valid():
                vle_id_instance = vle_basic_info_serializer.save()
                serialized_data = VleBasicInformationSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'Vle Id': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_basic_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleMobileNumberView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        vle_mobile_number_serializer = VleMobileNumberSerializer(data=request.data)
        try:
            if vle_mobile_number_serializer.is_valid():
                vle_id_instance = vle_mobile_number_serializer.save()
                serialized_data = VleMobileNumberSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'Vle Id': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_mobile_number_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PhotoOfBmcView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        photo_of_bmc_serializer = PhotoOfBmcSerializer(data=request.data)
        try:
            if photo_of_bmc_serializer.is_valid():
                vle_id_instance = photo_of_bmc_serializer.save()
                serialized_data = PhotoOfBmcSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')

                response_data = {
                    'Vle Id': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(photo_of_bmc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VLEBankDetailsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        vle_bank_details_serializer = VLEBankDetailsSerializer(data=request.data)
        try:
            if vle_bank_details_serializer.is_valid():
                vle_id_instance = vle_bank_details_serializer.save()
                serialized_data = VLEBankDetailsSerializer(vle_id_instance).data
                vle_id = serialized_data.get("vle_id")
                response_data = {
                    'Vle Id': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SkillsAndKnowledgeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        skills_and_knowledge_serializer = SkillsAndKnowledgeSerializer(data=request.data)
        try:
            if skills_and_knowledge_serializer.is_valid():
                vle_id_instance = skills_and_knowledge_serializer.save()
                serialized_data = SkillsAndKnowledgeSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'Vle Id':vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(skills_and_knowledge_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VLEEconomicAndSocialStatusInfoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        vle_eco_and_social_status_serializer = VLEEconomicAndSocialStatusInfoSerializer(data=request.data)
        try:
            if vle_eco_and_social_status_serializer.is_valid():
                vle_id_instance = vle_eco_and_social_status_serializer.save()
                serialized_data = VLEEconomicAndSocialStatusInfoSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'vle_id': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_eco_and_social_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleNearbyMilkCenterContactView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        vle_nearby_milk_center_serializer = VleNearbyMilkCenterContactSerializer(data=request.data)
        try:
            if vle_nearby_milk_center_serializer.is_valid():
                vle_id_instance = vle_nearby_milk_center_serializer.save()
                serialized_data = VleNearbyMilkCenterContactSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'Vle Id': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_nearby_milk_center_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VillageDetailsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        village_details_serializer = VillageDetailsSerializer(data=request.data)
        try:
            if village_details_serializer.is_valid():
                vle_id_instance = village_details_serializer.save()
                serialized_data = VillageDetailsSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'Vle Id': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(village_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)