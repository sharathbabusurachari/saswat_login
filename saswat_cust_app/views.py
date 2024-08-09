# import string
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404
# from .utils import is_valid_indian_mobile_number
from rest_framework.exceptions import ValidationError
from saswat_cust_app.models import (UserOtp, UserDetails, CustomerTest, Gender, State, VleVillageInfo,
                                    VleBasicInformation, VleMobileNumber, BmcBasicInformation, VLEBankDetails,
                                    VillageDetails, VleNearbyMilkCenterContact, VLEEconomicAndSocialStatusInfo,
                                    PhotoOfBmc, SkillsAndKnowledge,VleMobileVOtp,VleOtp, Country, District,
                                    DesignationDetails, WeekDetails, EmployeeDetails, EmployeeTargetDetails,
                                    EmployeeSetTargetDetails,
                                    LoanApplication, QueryModel, SignInSignOut, QnaAttachment, ShortenedQueries,
                                    ESign)

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from itertools import zip_longest
from random import randint
import random
from saswat_cust_app.serializers import (OTPSerializer, GpsSerializer, CustomerTestSerializer,
                                         GenderSerializer, StateSerializer,
                                         VleVillageInfoSerializer, BmcBasicInformationSerializer,
                                         VleBasicInformationSerializer, VleMobileNumberSerializer,
                                         PhotoOfBmcSerializer, VLEBankDetailsSerializer,
                                         SkillsAndKnowledgeSerializer, VLEEconomicAndSocialStatusInfoSerializer,
                                         VleNearbyMilkCenterContactSerializer,
                                         VillageDetailsSerializer, VleMobileVOtpSerializer, VleOtpSerializer,
                                         LoanApplicationSerializer, NewQuerySerializer,
                                         GetQuerySerializer, SignInSignOutSerializer, QnaAttachmentSerializer,
                                         EmployeeDetailsSerializer,
                                         ESignSerializer,
                                         QueryStatusUpdateSerializer)
from datetime import datetime, timedelta, date
import requests
# from rest_framework.authentication import SessionAuthentication
from .authenticate import MobileNumberAuthentication
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Subquery, OuterRef, Case, When, Value, IntegerField, Q, Sum, F
from django.db import connection
from django.shortcuts import render
from rest_framework.exceptions import APIException
from django.db import IntegrityError
import psycopg2
from django.db.models import Count
import json


class SendOTPAPIView(APIView):

    def post(self, request, *args, **kwargs):
        mobile_no = request.data.get('mobile_no')

        if not mobile_no:
            return Response({'status': '01', 'message': 'Mobile number is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        if mobile_no == "8888888888" or mobile_no == 8888888888:
            response_data = {
                'status': '00',
                'message': "OTP sent successfully",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            url = 'http://ci1.saswatfinance.com:8084/api/otp'
            try:
                if not UserDetails.objects.filter(mobile_no=mobile_no).exists():
                    response_data = {
                        'status': '01',
                        'message': "Mobile number does not exist",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)

                otp_code = str(random.randint(1000, 9999))
                data = {
                    'otp': otp_code,
                    'dest': mobile_no,
                    'msgName': "OTP"
                }

                response = requests.post(url, json=data)
                response.raise_for_status()
                if response.status_code == 200:
                    # Update existing OTP if it exists, otherwise create a new one
                    existing_otp = UserOtp.objects.filter(mobile_no=mobile_no).first()
                    if existing_otp:
                        existing_otp.otp_code = otp_code
                        existing_otp.otp_generation_time = timezone.now()
                        existing_otp.otp_expiration_time = timezone.now() + timedelta(minutes=10)  # Assuming 10 minutes expiry
                        existing_otp.save()
                    else:
                        UserOtp.objects.create(mobile_no=mobile_no, otp_code=otp_code)

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
                    return Response(response_data, status=status.HTTP_200_OK)

            except requests.exceptions.RequestException as e:
                return Response({'message': 'Error occurred while making the request'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'status': '01', 'message': f'An unexpected error occurred: {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def post(self, request, *args, **kwargs):
    #     mobile_no = request.data.get('mobile_no')
    #     if mobile_no == "8888888888" or mobile_no == 8888888888:
    #         response_data = {
    #             'status': '00',
    #             'message': "OTP sent successfully",
    #
    #         }
    #         return Response(response_data, status=status.HTTP_200_OK)
    #
    #     else:
    #
    #         url = 'http://ci1.saswatfinance.com:8084/api/otp'
    #         #url = 'http://20.235.255.141:8084/saswat/otp'
    #         try:
    #             existing_otp = UserOtp.objects.filter(mobile_no=mobile_no).order_by('otp_generation_time').first()
    #             if existing_otp is not None:
    #                 existing_otp.is_expired()
    #                 existing_otp.delete()
    #                 response_data = {
    #                     'status': '02',
    #                     'message': "An OTP has already been sent",
    #
    #                 }
    #                 return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    #
    #             # if not is_valid_indian_mobile_number(mobile_no):
    #             #     return JsonResponse({'error': 'Invalid Indian mobile number format'}, status=400)
    #             elif UserDetails.objects.filter(mobile_no=mobile_no).exists():
    #                 otp_code = str(random.randint(1000, 9999))
    #                 data = {
    #                     'otp': otp_code,
    #                     'dest': mobile_no,
    #                     'msgName': "OTP"
    #                 }
    #
    #                 response = requests.post(url, json=data)
    #                 if response.status_code == 200:
    #                     # result = response.json()
    #                     UserOtp.objects.create(mobile_no=str(mobile_no), otp_code=otp_code)
    #                     response_data = {
    #                         'status': '00',
    #                         'message': "OTP sent successfully",
    #
    #                     }
    #                     return Response(response_data, status=status.HTTP_200_OK)
    #                 else:
    #                     response_data = {
    #                         'status': '01',
    #                         'message': "Failed to send OTP to the user",
    #
    #                     }
    #                     return Response(response_data,
    #                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #             else:
    #                 response_data = {
    #                     'status': '01',
    #                     'message': "Mobile number does not exist",
    #
    #                 }
    #                 return Response(response_data, status=status.HTTP_200_OK)
    #         except requests.exceptions.RequestException as e:
    #             return Response({'message': 'Error occurred while making the request'},
    #                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidateOTPAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [MobileNumberAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            serializer = OTPSerializer(data=request.data)
            if serializer.is_valid():
                mobile_no = serializer.validated_data['mobile_no']
                otp_code = serializer.validated_data['otp_code']
                session_id = request.auth

                if (mobile_no == "8888888888" or mobile_no == 8888888888) and (otp_code == "1234" or otp_code == 1234):
                    user_det = UserDetails.objects.filter(mobile_no=mobile_no).first()
                    if user_det:
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
                        return Response(response_data, status=status.HTTP_200_OK)
                    else:
                        response_data = {
                            'status': '01',
                            'message': "Mobile number does not exist",
                        }
                        return JsonResponse(response_data, status=status.HTTP_200_OK)

                else:
                    user_det = UserDetails.objects.filter(mobile_no=mobile_no).first()
                    if user_det:
                        valid_otp = UserOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code).first()

                        if valid_otp:
                            if valid_otp.is_expired():
                                valid_otp.delete()
                                response_data = {
                                    'status': '01',
                                    'message': "OTP has expired.",
                                }
                                return Response(response_data, status=status.HTTP_200_OK)

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
                            valid_otp.delete()
                            return Response(response_data, status=status.HTTP_200_OK)

                        response_data = {
                            'status': '01',
                            'message': "Invalid OTP",
                        }
                        return JsonResponse(response_data, status=status.HTTP_200_OK)
                    else:
                        response_data = {
                            'status': '01',
                            'message': "Mobile number does not exist.",
                        }
                        return JsonResponse(response_data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'status': '02',
                'message': "An error occurred.",
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def post(self, request, *args, **kwargs):
    #     serializer = OTPSerializer(data=request.data)
    #     if serializer.is_valid():
    #         mobile_no = serializer.validated_data['mobile_no']
    #         otp_code = serializer.validated_data['otp_code']
    #         if (mobile_no == "8888888888" or mobile_no == 8888888888) and (otp_code == "1234" or otp_code == 1234):
    #             if UserDetails.objects.filter(mobile_no=mobile_no).exists():
    #                 user_det = UserDetails.objects.filter(mobile_no=mobile_no).first()
    #                 session_id = request.auth
    #                 response_data = {
    #                     'status': '00',
    #                     'message': "OTP verified successfully",
    #                     'session_id': session_id,
    #                     'user_id': user_det.user_id,
    #                     "first_name": user_det.first_name,
    #                     "mid_name": user_det.mid_name,
    #                     "last_name": user_det.last_name,
    #                     "work_dept": user_det.work_dept,
    #                     "mobile_no": user_det.mobile_no,
    #                     "designation": user_det.designation,
    #                     "designation_id": user_det.designation_id
    #                 }
    #                 return Response(response_data, status=200)
    #             else:
    #                 response_data = {
    #                     'status': '01',
    #                     'message': "Mobile number does not exist",
    #                 }
    #                 return JsonResponse(response_data, status=status.HTTP_200_OK)
    #
    #         else:
    #
    #             if UserDetails.objects.filter(mobile_no=mobile_no).exists():
    #                 check_valid_time = datetime.now() - timedelta(minutes=1)
    #                 user_det = UserDetails.objects.filter(mobile_no=mobile_no).first()
    #                 valid_otp_mobile = UserOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code).first()
    #                 valid_otp_time = UserOtp.objects.filter(mobile_no=mobile_no,
    #                                                         otp_expiration_time__lt=timezone.now()).first()
    #
    #                 verify_user_otp = UserOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code,
    #                                                          otp_generation_time__gte=check_valid_time).first()
    #                 session_id = request.auth
    #
    #                 # otp_instance = get_object_or_404(UserOtp, mobile_no=str(mobile_no), otp_code=otp_code)
    #                 if verify_user_otp:
    #                     response_data = {
    #                         'status': '00',
    #                         'message': "OTP verified successfully",
    #                         'session_id': session_id,
    #                         'user_id': user_det.user_id,
    #                         "first_name": user_det.first_name,
    #                         "mid_name": user_det.mid_name,
    #                         "last_name": user_det.last_name,
    #                         "work_dept": user_det.work_dept,
    #                         "mobile_no": user_det.mobile_no,
    #                         "designation": user_det.designation,
    #                         "designation_id": user_det.designation_id
    #                     }
    #                     verify_user_otp.delete()
    #                     return Response(response_data, status=200)
    #                 elif valid_otp_time:
    #                     response_data = {
    #                         'status': '01',
    #                         'message': "OTP has expired",
    #                     }
    #                     valid_otp_time.delete()
    #                     return Response(response_data, status=status.HTTP_200_OK)
    #                 elif valid_otp_mobile:
    #                     valid_otp_mobile.delete()
    #                 else:
    #                     response_data = {
    #                         'status': '01',
    #                         'message': "Invalid OTP",
    #                     }
    #                     return JsonResponse(response_data, status=status.HTTP_200_OK)
    #             else:
    #                 response_data = {
    #                     'status': '01',
    #                     'message': "Mobile number does not exist",
    #                 }
    #                 return JsonResponse(response_data, status=status.HTTP_200_OK)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def get(self, request, format=None):
        try:
            user_id = request.query_params.get('user_id')
            if not user_id:
                raise ValueError("User ID is not provided")

            village_info_data = VleVillageInfo.objects.filter(user_id=user_id).values('vle_id', 'village_name')
            basic_info_data = VleBasicInformation.objects.filter(user_id=user_id).values('vle_id', 'vle_name')
            basic_info_dict = {item['vle_id']: item for item in basic_info_data}

            common_data = []

            for vle_village_info in village_info_data:
                vle_id = vle_village_info['vle_id']
                village_name = vle_village_info['village_name']
                vle_name = basic_info_dict.get(vle_id, {}).get('vle_name', '')

                common_data.append({
                    'vle_id': vle_id,
                    'village_name': village_name,
                    'vle_name': vle_name
                })
            if not common_data:
                return Response({'status': '01', 'message': 'No data found for the provided user_id'}, status=status.HTTP_200_OK)

            response = {
                'status': '00',
                'message': 'success',
                'data': common_data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'status': '02', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # except VleVillageInfo.DoesNotExist or VleBasicInformation.DoesNotExist:
        #     return Response({'status': '03', 'message': 'User ID does not exist in the table'},
        #                     status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'status': '03', 'message': 'User ID does not exist in the table'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        vle_v_info_serializer = VleVillageInfoSerializer(data=request.data)
        try:
            if vle_v_info_serializer.is_valid():
                vle_id_instance = vle_v_info_serializer.save()
                response_data = {
                    'VleId': vle_id_instance.vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_v_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleBasicVillageInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                bmc_basic_queryset = VleVillageInfo.objects.filter(vle_id=vle_id)
                serializer = VleVillageInfoSerializer(bmc_basic_queryset, many=True)
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BmcBasicInformationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                bmc_basic_queryset = BmcBasicInformation.objects.filter(vle_id=vle_id)
                if not bmc_basic_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = BmcBasicInformationSerializer(bmc_basic_queryset, many=True)
                response_data = {
                    'status': '00',
                    'message': 'success',
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        bmc_basic_info_serializer = BmcBasicInformationSerializer(data=request.data)
        try:
            if bmc_basic_info_serializer.is_valid():
                vle_id_instance = bmc_basic_info_serializer.save()
                serialized_data = BmcBasicInformationSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')

                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(bmc_basic_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if vle_id:
                bmc_basic_instance = BmcBasicInformation.objects.filter(vle_id=vle_id).first()
                if not bmc_basic_instance:
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = BmcBasicInformationSerializer(bmc_basic_instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data = {
                        'VleId': vle_id,
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleBasicInformationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                vle_basic_queryset = VleBasicInformation.objects.filter(vle_id=vle_id)
                if not vle_basic_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = VleBasicInformationSerializer(vle_basic_queryset, many=True)
                response_data = {
                    'status': '00',
                    'message': "success",
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        vle_basic_info_serializer = VleBasicInformationSerializer(data=request.data)
        try:
            if vle_basic_info_serializer.is_valid():
                vle_id_instance = vle_basic_info_serializer.save()
                serialized_data = VleBasicInformationSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_basic_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if vle_id:
                vle_basic_info_instance = VleBasicInformation.objects.filter(vle_id=vle_id).first()
                if not vle_basic_info_instance:
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = VleBasicInformationSerializer(vle_basic_info_instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data = {
                        'VleId': vle_id,
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleMobileNumberView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                vle_mo_no_queryset = VleMobileNumber.objects.filter(vle_id=vle_id)
                if not vle_mo_no_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = VleMobileNumberSerializer(vle_mo_no_queryset, many=True)
                response_data = {
                    'status': '00',
                    'message': "success",
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        vle_mobile_number_serializer = VleMobileNumberSerializer(data=request.data)
        try:
            if vle_mobile_number_serializer.is_valid():
                vle_id_instance = vle_mobile_number_serializer.save()
                serialized_data = VleMobileNumberSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                try:
                    alternative_mobile_number = serialized_data.get('alternative_mobile_number')
                    alternate_data = {"alternate_mobile_number": alternative_mobile_number, "alternate_otp": "9999",
                                      "alternate_status": "Verified"}
                    alternate_data_list = [alternate_data]
                    vle_id_instance.status = 'Verified'
                    vle_id_instance.alternative_mobile_numbers = alternate_data_list
                    vle_id_instance.save()
                except Exception as e:
                    pass
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_mobile_number_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if vle_id:
                mo_no_instance = VleMobileNumber.objects.filter(vle_id=vle_id).first()
                if not mo_no_instance:
                    return Response({'error': 'VLE Mobile Number instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = VleMobileNumberSerializer(mo_no_instance, data=request.data, partial=True)
                if serializer.is_valid():
                    vle_id_instance = serializer.save()
                    try:
                        serialized_data = VleMobileNumberSerializer(vle_id_instance).data
                        alternative_mobile_number = serialized_data.get('alternative_mobile_number')
                        alternate_data = {"alternate_mobile_number": alternative_mobile_number, "alternate_otp": "9999",
                                          "alternate_status": "Verified"}
                        alternate_data_list = [alternate_data]
                        vle_id_instance.alternative_mobile_numbers = alternate_data_list
                        vle_id_instance.save()
                    except Exception as e:
                        pass
                    response_data = {
                        'VleId': vle_id,
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def post(self, request, *args, **kwargs):
    #     vle_mobile_number_serializer = VleMobileNumberSerializer(data=request.data)
    #     try:
    #         if vle_mobile_number_serializer.is_valid():
    #             vle_id_instance = vle_mobile_number_serializer.save()
    #             serialized_data = VleMobileNumberSerializer(vle_id_instance).data
    #             vle_id = serialized_data.get('vle_id')
    #             response_data = {
    #                 'VleId': vle_id,
    #                 'status': '00',
    #                 'message': "success",
    #             }
    #             return Response(response_data, status=status.HTTP_200_OK)
    #         else:
    #             return Response(vle_mobile_number_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # def put(self, request, *args, **kwargs):
    #     try:
    #         vle_id = request.data.get('vle_id')
    #         if vle_id:
    #             mo_no_instance = VleMobileNumber.objects.filter(vle_id=vle_id).first()
    #             if not mo_no_instance:
    #                 return Response({'error': 'VLE Mobile Number instance not found'},
    #                                 status=status.HTTP_404_NOT_FOUND)
    #
    #             serializer = VleMobileNumberSerializer(mo_no_instance, data=request.data, partial=True)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 response_data = {
    #                     'VleId': vle_id,
    #                     'status': '00',
    #                     'message': "success",
    #                 }
    #                 return Response(response_data, status=status.HTTP_200_OK)
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PhotoOfBmcView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if not vle_id:
                response_data = {
                    'status': '01',
                    'message': 'vle_id parameter is required',
                }
                return Response(response_data, status=status.HTTP_200_OK)

            photo_of_bmc_queryset = PhotoOfBmc.objects.filter(vle_id=vle_id)
            if not photo_of_bmc_queryset.exists():
                return Response({
                    'status': '01',
                    'msg': 'Data does not exist',
                    'data': []
                },status=status.HTTP_200_OK)
            serializer = PhotoOfBmcSerializer(photo_of_bmc_queryset, many=True)
            response_data = {
                'status': '00',
                'message': "success",
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'status': '01',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        photo_of_bmc_serializer = PhotoOfBmcSerializer(data=request.data, partial=True)
        try:
            if photo_of_bmc_serializer.is_valid():
                vle_id_instance = photo_of_bmc_serializer.save()
                serialized_data = PhotoOfBmcSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')

                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'status': '01',
                    'message': 'Validation Error',
                    'errors': photo_of_bmc_serializer.errors
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'status': '01',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if not vle_id:
                response_data = {
                    'status': '01',
                    'message': 'VLE Id parameter is required'
                }
                return Response(response_data, status=status.HTTP_200_OK)

            photo_bmc_instance = PhotoOfBmc.objects.filter(vle_id=vle_id).first()
            if not photo_bmc_instance:
                response_data = {
                    'status': '01',
                    'message': 'Photo Of Bmc instance not found'
                }
                return Response(response_data, status=status.HTTP_200_OK)

            serializer = PhotoOfBmcSerializer(photo_bmc_instance, data=request.data,  partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'status': '01',
                    'message': "Validation Error",
                    'errors': serializer.errors
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'status': '01',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class PhotoOfBmcView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request, format=None):
#         try:
#             vle_id = request.query_params.get('vle_id')
#             if vle_id:
#                 photo_of_bmc_queryset = PhotoOfBmc.objects.filter(vle_id=vle_id)
#                 if not photo_of_bmc_queryset.exists():
#                     return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
#                                     status=status.HTTP_200_OK)
#                 serializer = PhotoOfBmcSerializer(photo_of_bmc_queryset, many=True)
#                 response_data = {
#                     'status': '00',
#                     'message': "success",
#                     'data': serializer.data,
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
#         except ValueError as ve:
#             return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def post(self, request, *args, **kwargs):
#         photo_of_bmc_serializer = PhotoOfBmcSerializer(data=request.data)
#         try:
#             if photo_of_bmc_serializer.is_valid():
#                 vle_id_instance = photo_of_bmc_serializer.save()
#                 serialized_data = PhotoOfBmcSerializer(vle_id_instance).data
#                 vle_id = serialized_data.get('vle_id')
#
#                 response_data = {
#                     'VleId': vle_id,
#                     'status': '00',
#                     'message': "success",
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
#             else:
#                 return Response(photo_of_bmc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def put(self, request, *args, **kwargs):
#         try:
#             vle_id = request.data.get('vle_id')
#             if vle_id:
#                 photo_bmc_instance = PhotoOfBmc.objects.filter(vle_id=vle_id).first()
#                 if not photo_bmc_instance:
#                     return Response({'error': 'BmcBasicInformation instance not found'},
#                                     status=status.HTTP_404_NOT_FOUND)
#
#                 serializer = PhotoOfBmcSerializer(photo_bmc_instance, data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     response_data = {
#                         'VleId': vle_id,
#                         'status': '00',
#                         'message': "success",
#                     }
#                     return Response(response_data, status=status.HTTP_200_OK)
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VLEBankDetailsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                vle_bank_det_queryset = VLEBankDetails.objects.filter(vle_id=vle_id)
                if not vle_bank_det_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = VLEBankDetailsSerializer(vle_bank_det_queryset, many=True)
                response_data = {
                    'status': '00',
                    'message': "success",
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        vle_bank_details_serializer = VLEBankDetailsSerializer(data=request.data)
        try:
            if vle_bank_details_serializer.is_valid():
                vle_id_instance = vle_bank_details_serializer.save()
                serialized_data = VLEBankDetailsSerializer(vle_id_instance).data
                vle_id = serialized_data.get("vle_id")
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if vle_id:
                vle_bank_det_instance = VLEBankDetails.objects.filter(vle_id=vle_id).first()
                if not vle_bank_det_instance:
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = VLEBankDetailsSerializer(vle_bank_det_instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data = {
                        'VleId': vle_id,
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SkillsAndKnowledgeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                skill_and_kno_queryset = SkillsAndKnowledge.objects.filter(vle_id=vle_id)
                if not skill_and_kno_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = SkillsAndKnowledgeSerializer(skill_and_kno_queryset, many=True)
                response_data = {
                    'status': '00',
                    'message': "success",
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        skills_and_knowledge_serializer = SkillsAndKnowledgeSerializer(data=request.data)
        try:
            if skills_and_knowledge_serializer.is_valid():
                vle_id_instance = skills_and_knowledge_serializer.save()
                serialized_data = SkillsAndKnowledgeSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(skills_and_knowledge_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if vle_id:
                sk_and_kno_instance = SkillsAndKnowledge.objects.filter(vle_id=vle_id).first()
                if not sk_and_kno_instance:
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = SkillsAndKnowledgeSerializer(sk_and_kno_instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data = {
                        'VleId': vle_id,
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VLEEconomicAndSocialStatusInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                vle_eco_queryset = VLEEconomicAndSocialStatusInfo.objects.filter(vle_id=vle_id)
                if not vle_eco_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = VLEEconomicAndSocialStatusInfoSerializer(vle_eco_queryset, many=True)
                response_data = {
                    'status': '00',
                    'message': 'success',
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        vle_eco_and_social_status_serializer = VLEEconomicAndSocialStatusInfoSerializer(data=request.data)
        try:
            if vle_eco_and_social_status_serializer.is_valid():
                vle_id_instance = vle_eco_and_social_status_serializer.save()
                serialized_data = VLEEconomicAndSocialStatusInfoSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_eco_and_social_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if vle_id:
                eco_and_soc_instance = VLEEconomicAndSocialStatusInfo.objects.filter(vle_id=vle_id).first()
                if not eco_and_soc_instance:
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = VLEEconomicAndSocialStatusInfoSerializer(eco_and_soc_instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data = {
                        'VleId': vle_id,
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleNearbyMilkCenterContactView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                vle_near_queryset = VleNearbyMilkCenterContact.objects.filter(vle_id=vle_id)
                if not vle_near_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = VleNearbyMilkCenterContactSerializer(vle_near_queryset, many=True)
                response_data = {
                    'status': '00',
                    'message': 'success',
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        vle_nearby_milk_center_serializer = VleNearbyMilkCenterContactSerializer(data=request.data)
        try:
            if vle_nearby_milk_center_serializer.is_valid():
                vle_id_instance = vle_nearby_milk_center_serializer.save()
                serialized_data = VleNearbyMilkCenterContactSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(vle_nearby_milk_center_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            new_remark = request.data.get('new_remark')
            mobile_number = new_remark.get("Mobile Number")
            name_of_the_person = new_remark.get("Name Of the Person")
            add_of_the_milk_center = new_remark.get("Address of the Milk Center")
            print(vle_id,mobile_number ,name_of_the_person, add_of_the_milk_center)

            if vle_id:
                milk_center_instance = VleNearbyMilkCenterContact.objects.filter(vle_id=vle_id).first()
                if not milk_center_instance:
                    vle_village_info = VleVillageInfo.objects.get(vle_id=vle_id)
                    user_id = VleVillageInfo.objects.filter(vle_id=vle_id).values('user_id')
                    if vle_village_info is not None:
                        VleNearbyMilkCenterContact.objects.create(vle_id=vle_village_info,mobile_number=mobile_number,name=name_of_the_person,
                                                                  address=add_of_the_milk_center,user_id=user_id)
                    response_data = {
                        'VleId': vle_id,
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)

                user_id_dict = VleVillageInfo.objects.filter(vle_id=vle_id).values('user_id').first()

                if user_id_dict:
                    user_id = user_id_dict['user_id']  # This should be a string or valid value

                    serializer = VleNearbyMilkCenterContactSerializer(milk_center_instance, data=request.data,
                                                                      partial=True)
                    if serializer.is_valid():
                        milk_center_instance.user_id = user_id  # Set user_id as a string value
                        serializer.save()  # Save the rest of the fields
                        response_data = {
                            'VleId': vle_id,
                            'status': '00',
                            'message': "success",
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VillageDetailsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                village_det_queryset = VillageDetails.objects.filter(vle_id=vle_id)
                if not village_det_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = VillageDetailsSerializer(village_det_queryset, many=True)
                response_data = {
                    'status': '00',
                    'message': 'success',
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        village_details_serializer = VillageDetailsSerializer(data=request.data)
        try:
            if village_details_serializer.is_valid():
                vle_id_instance = village_details_serializer.save()
                serialized_data = VillageDetailsSerializer(vle_id_instance).data
                vle_id = serialized_data.get('vle_id')
                response_data = {
                    'VleId': vle_id,
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(village_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if vle_id:
                vill_det_instance = VillageDetails.objects.filter(vle_id=vle_id).first()
                if not vill_det_instance:
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = VillageDetailsSerializer(vill_det_instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data = {
                        'VleId': vle_id,
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'vle_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------


# class VleMobileVerificationView(APIView):
#     def post(self, request, *args, **kwargs):
#         vle_mobile_number = request.data.get('mobile_no')
#         vle_id = request.data.get('vle_id')
#         user_id = request.data.get('user_id')
#         primary_or_secondary = request.data.get('primary_or_secondary')
#         url = 'http://ci1.saswatfinance.com:8084/api/otp'
#
#         try:
#             # mobile_exists = VleMobileNumber.objects.filter(vle_mobile_number=vle_mobile_number,
#             #                                                status="Verified").exists()
#             mobile_exists = VleMobileNumber.objects.filter(vle_mobile_number=vle_mobile_number,
#                                                            status="Verified").exists()
#             mobile_exists_1 = VleMobileNumber.objects.filter(vle_mobile_number=vle_mobile_number,
#                                                              status="Not Verified").exists()
#             another_mobile_exists = VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).exists()
#             unverified_mobile_exists = VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id,
#                                                                       vle_mobile_number=vle_mobile_number,
#                                                                       status="Not Verified").exists()
#             if primary_or_secondary == 1:
#                 if mobile_exists:
#                     response_data = {
#                         'status': '01',
#                         'message': "Mobile Number already exists, Please enter another number.",
#
#                     }
#                     return Response(response_data, status=status.HTTP_200_OK)
#                 elif another_mobile_exists or unverified_mobile_exists:
#                     existing_otp = VleOtp.objects.filter(mobile_no=vle_mobile_number)
#                     if existing_otp.exists():
#                         try:
#                             existing_otp.delete()
#                             otp_code = str(random.randint(1000, 9999))
#                             if another_mobile_exists:
#                                 VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).delete()
#                                 VleMobileNumber.objects.create(vle_id_id=vle_id, user_id=user_id,
#                                                                vle_mobile_number=vle_mobile_number, otp=otp_code,
#                                                                status="Not Verified")
#                             if unverified_mobile_exists:
#                                 VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id,
#                                                                vle_mobile_number=vle_mobile_number,
#                                                                status="Not Verified").delete()
#                                 VleMobileNumber.objects.create(vle_id_id=vle_id, user_id=user_id,
#                                                                vle_mobile_number=vle_mobile_number,
#                                                                status="Not Verified", otp=otp_code)
#                             data = {
#                                 'otp': otp_code,
#                                 'dest': vle_mobile_number,
#                             }
#                             response = requests.post(url, json=data)
#                             if response.status_code == 200:
#                                 VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
#                                                       vle_id_id=vle_id, user_id=user_id)
#                                 response_data = {
#                                     'vle_id': vle_id,
#                                     'status': '00',
#                                     'message': "OTP sent successfully",
#                                 }
#                                 return Response(response_data, status=status.HTTP_200_OK)
#                             else:
#                                 response_data = {
#                                     'status': '01',
#                                     'message': "Failed to send OTP to the user",
#
#                                 }
#                                 return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                         except Exception as e:
#                             # print("Error deleting existing OTPs:", e)
#                             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                     else:
#                         existing_otp = VleOtp.objects.filter(vle_id_id=vle_id)
#                         if existing_otp.exists():
#                             existing_otp.delete()
#                         otp_code = str(random.randint(1000, 9999))
#                         if another_mobile_exists:
#                             VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).delete()
#                             VleMobileNumber.objects.create(vle_id_id=vle_id, user_id=user_id,
#                                                            vle_mobile_number=vle_mobile_number, otp=otp_code,
#                                                            status="Not Verified")
#                         if unverified_mobile_exists:
#                             VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id,
#                                                            vle_mobile_number=vle_mobile_number,
#                                                            status="Not Verified").delete()
#                             VleMobileNumber.objects.create(vle_id_id=vle_id, user_id=user_id,
#                                                            vle_mobile_number=vle_mobile_number,
#                                                            status="Not Verified", otp=otp_code)
#                         data = {
#                             'otp': otp_code,
#                             'dest': vle_mobile_number,
#                         }
#                         response = requests.post(url, json=data)
#                         if response.status_code == 200:
#                             VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
#                                                   vle_id_id=vle_id, user_id=user_id)
#                             response_data = {
#                                 'vle_id': vle_id,
#                                 'status': '00',
#                                 'message': "OTP sent successfully",
#                             }
#                             return Response(response_data, status=status.HTTP_200_OK)
#                         else:
#                             response_data = {
#                                 'status': '01',
#                                 'message': "Failed to send OTP to the user",
#
#                             }
#                             return Response(response_data,
#                                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                 else:
#                     existing_otp = VleOtp.objects.filter(mobile_no=vle_mobile_number)
#                     if existing_otp.exists():
#                         try:
#                             existing_otp.delete()
#                             otp_code = str(random.randint(1000, 9999))
#                             VleMobileNumber.objects.create(vle_mobile_number=vle_mobile_number, otp=otp_code,
#                                                            vle_id_id=vle_id, user_id=user_id, status="Not Verified")
#                             data = {
#                                 'otp': otp_code,
#                                 'dest': vle_mobile_number,
#                             }
#                             response = requests.post(url, json=data)
#                             if response.status_code == 200:
#                                 VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
#                                                       vle_id_id=vle_id, user_id=user_id)
#                                 response_data = {
#                                     'vle_id': vle_id,
#                                     'status': '00',
#                                     'message': "OTP sent successfully",
#                                 }
#                                 return Response(response_data, status=status.HTTP_200_OK)
#                             else:
#                                 response_data = {
#                                     'status': '01',
#                                     'message': "Failed to send OTP to the user",
#
#                                 }
#                                 return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                         except Exception as e:
#                             # print("Error deleting existing OTPs:", e)
#                             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                     else:
#                         existing_otp = VleOtp.objects.filter(vle_id_id=vle_id)
#                         if existing_otp.exists():
#                             existing_otp.delete()
#                         otp_code = str(random.randint(1000, 9999))
#                         VleMobileNumber.objects.create(vle_mobile_number=vle_mobile_number, otp=otp_code,
#                                                        vle_id_id=vle_id, user_id=user_id, status="Not Verified")
#                         data = {
#                             'otp': otp_code,
#                             'dest': vle_mobile_number,
#                         }
#                         response = requests.post(url, json=data)
#                         if response.status_code == 200:
#                             VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
#                                                   vle_id_id=vle_id, user_id=user_id)
#                             response_data = {
#                                 'vle_id': vle_id,
#                                 'status': '00',
#                                 'message': "OTP sent successfully",
#                             }
#                             return Response(response_data, status=status.HTTP_200_OK)
#                         else:
#                             response_data = {
#                                 'status': '01',
#                                 'message': "Failed to send OTP to the user",
#
#                             }
#                             return Response(response_data,
#                                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             elif primary_or_secondary == -1:
#                 primary_exists = VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).first()
#                 if not primary_exists:
#                     return Response({'error': 'Enter Primary Mobile Number first.'},
#                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                 elif mobile_exists:
#                     response_data = {
#                         'status': '01',
#                         'message': "Mobile Number already exists, Please enter another number.",
#
#                     }
#                     return Response(response_data, status=status.HTTP_200_OK)
#                 elif mobile_exists_1:
#                     response_data = {
#                         'status': '01',
#                         'message': "Mobile Number already exists, Please enter another number.",
#
#                     }
#                     return Response(response_data, status=status.HTTP_200_OK)
#                 elif primary_exists:
#                     alternative_numbers_column = primary_exists.alternative_mobile_numbers
#                     primary_mobile_number = primary_exists.vle_mobile_number
#                     existing_otp = VleOtp.objects.filter(mobile_no=primary_mobile_number)
#                     if existing_otp.exists():
#                         try:
#                             existing_otp.delete()
#                             otp_code = str(random.randint(1000, 9999))
#                             alternate_data = {"alternate_mobile_number": vle_mobile_number, "alternate_otp": otp_code,
#                                               "alternate_status": "Not Verified"}
#                             if isinstance(alternative_numbers_column, list) and not alternative_numbers_column:
#                                 alternate_data_list = [alternate_data]
#                                 VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
#                                     alternative_mobile_numbers=alternate_data_list)
#                             elif alternative_numbers_column and isinstance(alternative_numbers_column, list):
#                                 already = False
#                                 for number_entry in alternative_numbers_column:
#                                     if (number_entry['alternate_mobile_number'] == vle_mobile_number and
#                                             number_entry['alternate_status'] == "Verified"):
#                                         already = True
#                                 if already:
#                                     response_data = {
#                                         'status': '01',
#                                         'message': "Mobile Number already exists, Please enter another number.",
#
#                                     }
#                                     return Response(response_data, status=status.HTTP_200_OK)
#                                 updated = False
#                                 for number_entry in alternative_numbers_column:
#                                     if (number_entry['alternate_mobile_number'] == vle_mobile_number and
#                                             number_entry['alternate_status'] == "Not Verified"):
#                                         number_entry['alternate_otp'] = otp_code
#                                         updated = True
#                                 if updated:
#                                     primary_exists.save()
#                                 else:
#                                     alternative_numbers_column.append(alternate_data)
#                                     VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
#                                         alternative_mobile_numbers=alternative_numbers_column)
#                             else:
#                                 alternate_data_list = [alternate_data]
#                                 VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
#                                     alternative_mobile_numbers=alternate_data_list)
#                             data = {
#                                 'otp': otp_code,
#                                 'dest': vle_mobile_number,
#                             }
#                             response = requests.post(url, json=data)
#                             if response.status_code == 200:
#                                 VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
#                                                       vle_id_id=vle_id, user_id=user_id)
#                                 response_data = {
#                                     'vle_id': vle_id,
#                                     'status': '00',
#                                     'message': "OTP sent successfully",
#                                 }
#                                 return Response(response_data, status=status.HTTP_200_OK)
#                             else:
#                                 response_data = {
#                                     'status': '01',
#                                     'message': "Failed to send OTP to the user",
#
#                                 }
#                                 return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                         except Exception as e:
#                             # print("Error deleting existing OTPs:", e)
#                             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                     else:
#                         existing_otp = VleOtp.objects.filter(vle_id_id=vle_id)
#                         if existing_otp.exists():
#                             existing_otp.delete()
#                         otp_code = str(random.randint(1000, 9999))
#                         alternate_data = {"alternate_mobile_number": vle_mobile_number, "alternate_otp": otp_code,
#                                           "alternate_status": "Not Verified"}
#                         if isinstance(alternative_numbers_column, list) and not alternative_numbers_column:
#                             alternate_data_list = [alternate_data]
#                             VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
#                                 alternative_mobile_numbers=alternate_data_list)
#                         elif alternative_numbers_column and isinstance(alternative_numbers_column, list):
#                             already = False
#                             for number_entry in alternative_numbers_column:
#                                 if (number_entry['alternate_mobile_number'] == vle_mobile_number and
#                                         number_entry['alternate_status'] == "Verified"):
#                                     already = True
#                             if already:
#                                 response_data = {
#                                     'status': '01',
#                                     'message': "Mobile Number already exists, Please enter another number.",
#
#                                 }
#                                 return Response(response_data, status=status.HTTP_200_OK)
#                             updated = False
#                             for number_entry in alternative_numbers_column:
#                                 if (number_entry['alternate_mobile_number'] == vle_mobile_number and
#                                         number_entry['alternate_status'] == "Not Verified"):
#                                     number_entry['alternate_otp'] = otp_code
#                                     updated = True
#                             if updated:
#                                 primary_exists.save()
#                             else:
#                                 alternative_numbers_column.append(alternate_data)
#                                 VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
#                                     alternative_mobile_numbers=alternative_numbers_column)
#                         else:
#                             alternate_data_list = [alternate_data]
#                             VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
#                                 alternative_mobile_numbers=alternate_data_list)
#                         data = {
#                             'otp': otp_code,
#                             'dest': vle_mobile_number,
#                         }
#                         response = requests.post(url, json=data)
#                         if response.status_code == 200:
#                             VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
#                                                   vle_id_id=vle_id, user_id=user_id)
#                             response_data = {
#                                 'vle_id': vle_id,
#                                 'status': '00',
#                                 'message': "OTP sent successfully",
#                             }
#                             return Response(response_data, status=status.HTTP_200_OK)
#                         else:
#                             response_data = {
#                                 'status': '01',
#                                 'message': "Failed to send OTP to the user",
#
#                             }
#                             return Response(response_data,
#                                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except IntegrityError as e:
#             if isinstance(e.__cause__, psycopg2.errors.UniqueViolation):
#                 return Response({'error': 'Provided VLE ID already exists'},
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             else:
#                 return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except requests.exceptions.RequestException as e:
#             return Response({'error': 'Error occurred while making the request'},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# class VleValidateOTPAPIView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         mobile_no = request.data.get('mobile_no')
#         otp_code = request.data.get('otp_code')
#         vle_id = request.data.get('vle_id')
#         primary_or_secondary = request.data.get('primary_or_secondary')
#         if VleOtp.objects.filter(mobile_no=mobile_no).exists():
#             if VleOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code).exists():
#                 response_data = {
#                     'status': '00',
#                     'message': "OTP verified successfully",
#                     'vle_id': vle_id
#                 }
#                 if primary_or_secondary == 1:
#                     VleMobileNumber.objects.filter(vle_id_id=vle_id).update(status="Verified")
#                 elif primary_or_secondary == -1:
#                     primary_exists = VleMobileNumber.objects.filter(vle_id_id=vle_id).first()
#                     if not primary_exists:
#                         return Response({'error': 'Primary Mobile Number Does Not Exist.'},
#                                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                     elif primary_exists:
#                         alternative_numbers_column = primary_exists.alternative_mobile_numbers
#                         if isinstance(alternative_numbers_column, list) and not alternative_numbers_column:
#                             return Response({'error': 'Alternate Number Not Found.'},
#                                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                         elif alternative_numbers_column and isinstance(alternative_numbers_column, list):
#                             updated = False
#                             for number_entry in alternative_numbers_column:
#                                 if (number_entry['alternate_mobile_number'] == mobile_no and
#                                         number_entry['alternate_status'] == "Not Verified"):
#                                     number_entry['alternate_status'] = "Verified"
#                                     updated = True
#                             if updated:
#                                 primary_exists.save()
#                             else:
#                                 return Response({'error': 'Alternate Number Not Found.'},
#                                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                         else:
#                             return Response({'error': 'Alternate Number Not Found'},
#                                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                 return Response(response_data, status=200)
#             else:
#                 response_data = {
#                     'status': '01',
#                     'message': "Invalid OTP",
#                 }
#                 return JsonResponse(response_data, status=status.HTTP_200_OK)
#         else:
#             response_data = {
#                 'status': '01',
#                 'message': "Mobile number does not exist, Please Resend OTP.",
#             }
#             return JsonResponse(response_data, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VleMobileVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        vle_mobile_number = request.data.get('mobile_no')
        vle_id = request.data.get('vle_id')
        user_id = request.data.get('user_id')
        primary_or_secondary = request.data.get('primary_or_secondary')
        url = 'http://ci1.saswatfinance.com:8084/api/otp'

        try:
            if primary_or_secondary:
                # mobile_exists = VleMobileNumber.objects.filter(vle_mobile_number=vle_mobile_number,
                #                                                status="Verified").exists()
                mobile_exists = VleMobileNumber.objects.filter(vle_mobile_number=vle_mobile_number,
                                                               status="Verified").exists()
                mobile_exists_1 = VleMobileNumber.objects.filter(vle_mobile_number=vle_mobile_number,
                                                                 status="Not Verified").exists()
                another_mobile_exists = VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).exists()
                unverified_mobile_exists = VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id,
                                                                          vle_mobile_number=vle_mobile_number,
                                                                          status="Not Verified").exists()
                if primary_or_secondary == 1:
                    if mobile_exists:
                        response_data = {
                            'status': '01',
                            'message': "Mobile Number already exists, Please enter another number.",

                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    elif another_mobile_exists or unverified_mobile_exists:
                        existing_otp = VleOtp.objects.filter(mobile_no=vle_mobile_number)
                        if existing_otp.exists():
                            try:
                                existing_otp.delete()
                                otp_code = str(random.randint(1000, 9999))
                                if another_mobile_exists:
                                    VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).delete()
                                    VleMobileNumber.objects.create(vle_id_id=vle_id, user_id=user_id,
                                                                   vle_mobile_number=vle_mobile_number, otp=otp_code,
                                                                   status="Not Verified")
                                if unverified_mobile_exists:
                                    VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id,
                                                                   vle_mobile_number=vle_mobile_number,
                                                                   status="Not Verified").delete()
                                    VleMobileNumber.objects.create(vle_id_id=vle_id, user_id=user_id,
                                                                   vle_mobile_number=vle_mobile_number,
                                                                   status="Not Verified", otp=otp_code)
                                data = {
                                    'otp': otp_code,
                                    'dest': vle_mobile_number,
                                }
                                response = requests.post(url, json=data)
                                if response.status_code == 200:
                                    VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
                                                          vle_id_id=vle_id, user_id=user_id)
                                    response_data = {
                                        'vle_id': vle_id,
                                        'status': '00',
                                        'message': "OTP sent successfully",
                                    }
                                    return Response(response_data, status=status.HTTP_200_OK)
                                else:
                                    response_data = {
                                        'status': '01',
                                        'message': "Failed to send OTP to the user",

                                    }
                                    return Response(response_data, status=status.HTTP_200_OK)
                            except Exception as e:
                                # print("Error deleting existing OTPs:", e)
                                response_data = {
                                    'status': '01',
                                    'message': "Some error occurred, Please try again.",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                                #return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            existing_otp = VleOtp.objects.filter(vle_id_id=vle_id)
                            if existing_otp.exists():
                                existing_otp.delete()
                            otp_code = str(random.randint(1000, 9999))
                            if another_mobile_exists:
                                VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).delete()
                                VleMobileNumber.objects.create(vle_id_id=vle_id, user_id=user_id,
                                                               vle_mobile_number=vle_mobile_number, otp=otp_code,
                                                               status="Not Verified")
                            if unverified_mobile_exists:
                                VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id,
                                                               vle_mobile_number=vle_mobile_number,
                                                               status="Not Verified").delete()
                                VleMobileNumber.objects.create(vle_id_id=vle_id, user_id=user_id,
                                                               vle_mobile_number=vle_mobile_number,
                                                               status="Not Verified", otp=otp_code)
                            data = {
                                'otp': otp_code,
                                'dest': vle_mobile_number,
                            }
                            response = requests.post(url, json=data)
                            if response.status_code == 200:
                                VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
                                                      vle_id_id=vle_id, user_id=user_id)
                                response_data = {
                                    'vle_id': vle_id,
                                    'status': '00',
                                    'message': "OTP sent successfully",
                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                            else:
                                response_data = {
                                    'status': '01',
                                    'message': "Failed to send OTP to the user",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                    else:
                        existing_otp = VleOtp.objects.filter(mobile_no=vle_mobile_number)
                        if existing_otp.exists():
                            try:
                                existing_otp.delete()
                                otp_code = str(random.randint(1000, 9999))
                                VleMobileNumber.objects.create(vle_mobile_number=vle_mobile_number, otp=otp_code,
                                                               vle_id_id=vle_id, user_id=user_id, status="Not Verified")
                                data = {
                                    'otp': otp_code,
                                    'dest': vle_mobile_number,
                                }
                                response = requests.post(url, json=data)
                                if response.status_code == 200:
                                    VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
                                                          vle_id_id=vle_id, user_id=user_id)
                                    response_data = {
                                        'vle_id': vle_id,
                                        'status': '00',
                                        'message': "OTP sent successfully",
                                    }
                                    return Response(response_data, status=status.HTTP_200_OK)
                                else:
                                    response_data = {
                                        'status': '01',
                                        'message': "Failed to send OTP to the user",

                                    }
                                    return Response(response_data, status=status.HTTP_200_OK)
                            except Exception as e:
                                # print("Error deleting existing OTPs:", e)
                                response_data = {
                                    'status': '01',
                                    'message': "Some error occurred, Please try again.",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                                #return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            existing_otp = VleOtp.objects.filter(vle_id_id=vle_id)
                            if existing_otp.exists():
                                existing_otp.delete()
                            otp_code = str(random.randint(1000, 9999))
                            VleMobileNumber.objects.create(vle_mobile_number=vle_mobile_number, otp=otp_code,
                                                           vle_id_id=vle_id, user_id=user_id, status="Not Verified")
                            data = {
                                'otp': otp_code,
                                'dest': vle_mobile_number,
                            }
                            response = requests.post(url, json=data)
                            if response.status_code == 200:
                                VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
                                                      vle_id_id=vle_id, user_id=user_id)
                                response_data = {
                                    'vle_id': vle_id,
                                    'status': '00',
                                    'message': "OTP sent successfully",
                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                            else:
                                response_data = {
                                    'status': '01',
                                    'message': "Failed to send OTP to the user",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                elif primary_or_secondary == -1:
                    primary_exists = VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).first()
                    if not primary_exists:
                        response_data = {
                            'status': '01',
                            'message': "Enter Primary Mobile Number first.",

                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                        # return Response({'error': 'Enter Primary Mobile Number first.'},
                        #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    elif mobile_exists:
                        response_data = {
                            'status': '01',
                            'message': "Mobile Number already exists, Please enter another number.",

                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    elif mobile_exists_1:
                        response_data = {
                            'status': '01',
                            'message': "Mobile Number already exists, Please enter another number.",

                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    elif primary_exists:
                        alternative_numbers_column = primary_exists.alternative_mobile_numbers
                        primary_mobile_number = primary_exists.vle_mobile_number
                        existing_otp = VleOtp.objects.filter(mobile_no=primary_mobile_number)
                        if existing_otp.exists():
                            try:
                                existing_otp.delete()
                                otp_code = str(random.randint(1000, 9999))
                                alternate_data = {"alternate_mobile_number": vle_mobile_number, "alternate_otp": otp_code,
                                                  "alternate_status": "Not Verified"}
                                if isinstance(alternative_numbers_column, list) and not alternative_numbers_column:
                                    alternate_data_list = [alternate_data]
                                    VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
                                        alternative_mobile_numbers=alternate_data_list)
                                elif alternative_numbers_column and isinstance(alternative_numbers_column, list):
                                    already = False
                                    for number_entry in alternative_numbers_column:
                                        if (number_entry['alternate_mobile_number'] == vle_mobile_number and
                                                number_entry['alternate_status'] == "Verified"):
                                            already = True
                                    if already:
                                        response_data = {
                                            'status': '01',
                                            'message': "Mobile Number already exists, Please enter another number.",

                                        }
                                        return Response(response_data, status=status.HTTP_200_OK)
                                    updated = False
                                    for number_entry in alternative_numbers_column:
                                        if (number_entry['alternate_mobile_number'] == vle_mobile_number and
                                                number_entry['alternate_status'] == "Not Verified"):
                                            number_entry['alternate_otp'] = otp_code
                                            updated = True
                                    if updated:
                                        primary_exists.save()
                                    else:
                                        alternative_numbers_column.append(alternate_data)
                                        VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
                                            alternative_mobile_numbers=alternative_numbers_column)
                                else:
                                    alternate_data_list = [alternate_data]
                                    VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
                                        alternative_mobile_numbers=alternate_data_list)
                                data = {
                                    'otp': otp_code,
                                    'dest': vle_mobile_number,
                                }
                                response = requests.post(url, json=data)
                                if response.status_code == 200:
                                    VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
                                                          vle_id_id=vle_id, user_id=user_id)
                                    response_data = {
                                        'vle_id': vle_id,
                                        'status': '00',
                                        'message': "OTP sent successfully",
                                    }
                                    return Response(response_data, status=status.HTTP_200_OK)
                                else:
                                    response_data = {
                                        'status': '01',
                                        'message': "Failed to send OTP to the user",

                                    }
                                    return Response(response_data, status=status.HTTP_200_OK)
                            except Exception as e:
                                # print("Error deleting existing OTPs:", e)
                                response_data = {
                                    'status': '01',
                                    'message': "Some error occurred, Please try again.",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                                # return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            existing_otp = VleOtp.objects.filter(vle_id_id=vle_id)
                            if existing_otp.exists():
                                existing_otp.delete()
                            otp_code = str(random.randint(1000, 9999))
                            alternate_data = {"alternate_mobile_number": vle_mobile_number, "alternate_otp": otp_code,
                                              "alternate_status": "Not Verified"}
                            if isinstance(alternative_numbers_column, list) and not alternative_numbers_column:
                                alternate_data_list = [alternate_data]
                                VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
                                    alternative_mobile_numbers=alternate_data_list)
                            elif alternative_numbers_column and isinstance(alternative_numbers_column, list):
                                already = False
                                for number_entry in alternative_numbers_column:
                                    if (number_entry['alternate_mobile_number'] == vle_mobile_number and
                                            number_entry['alternate_status'] == "Verified"):
                                        already = True
                                if already:
                                    response_data = {
                                        'status': '01',
                                        'message': "Mobile Number already exists, Please enter another number.",

                                    }
                                    return Response(response_data, status=status.HTTP_200_OK)
                                updated = False
                                for number_entry in alternative_numbers_column:
                                    if (number_entry['alternate_mobile_number'] == vle_mobile_number and
                                            number_entry['alternate_status'] == "Not Verified"):
                                        number_entry['alternate_otp'] = otp_code
                                        updated = True
                                if updated:
                                    primary_exists.save()
                                else:
                                    alternative_numbers_column.append(alternate_data)
                                    VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
                                        alternative_mobile_numbers=alternative_numbers_column)
                            else:
                                alternate_data_list = [alternate_data]
                                VleMobileNumber.objects.filter(vle_id_id=vle_id, user_id=user_id).update(
                                    alternative_mobile_numbers=alternate_data_list)
                            data = {
                                'otp': otp_code,
                                'dest': vle_mobile_number,
                            }
                            response = requests.post(url, json=data)
                            if response.status_code == 200:
                                VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
                                                      vle_id_id=vle_id, user_id=user_id)
                                response_data = {
                                    'vle_id': vle_id,
                                    'status': '00',
                                    'message': "OTP sent successfully",
                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                            else:
                                response_data = {
                                    'status': '01',
                                    'message': "Failed to send OTP to the user",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
            else:
                mobile_exists = VleMobileNumber.objects.filter(vle_mobile_number=vle_mobile_number).exists()
                if mobile_exists:
                    response_data = {
                        'status': '01',
                        'message': "Mobile Number already exists, Please enter another number.",

                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:

                    existing_otp = VleOtp.objects.filter(mobile_no=vle_mobile_number)
                    if existing_otp.exists():
                        try:
                            existing_otp.delete()
                            otp_code = str(random.randint(1000, 9999))
                            # VleMobileNumber.objects.create(vle_mobile_number=vle_mobile_number, otp=otp_code,
                            #                                vle_id_id=vle_id, user_id=user_id)
                            data = {
                                'otp': otp_code,
                                'dest': vle_mobile_number,
                            }
                            response = requests.post(url, json=data)
                            if response.status_code == 200:
                                VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code,
                                                      vle_id_id=vle_id, user_id=user_id)
                                response_data = {
                                    'vle_id': vle_id,
                                    'status': '00',
                                    'message': "OTP sent successfully",
                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                            else:
                                response_data = {
                                    'status': '01',
                                    'message': "Failed to send OTP to the user",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                        except Exception as e:
                            # print("Error deleting existing OTPs:", e)
                            response_data = {
                                'status': '01',
                                'message': "Some error occurred, Please try again.",

                            }
                            return Response(response_data, status=status.HTTP_200_OK)
                    else:
                        existing_otp = VleOtp.objects.filter(vle_id_id=vle_id)
                        if existing_otp.exists():
                            existing_otp.delete()

                        otp_code = str(random.randint(1000, 9999))
                        # VleMobileNumber.objects.create(vle_mobile_number=vle_mobile_number, otp=otp_code,
                        #                                vle_id_id=vle_id, user_id=user_id)
                        data = {
                            'otp': otp_code,
                            'dest': vle_mobile_number,
                        }
                        response = requests.post(url, json=data)
                        if response.status_code == 200:
                            VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code, vle_id_id=vle_id,
                                                  user_id=user_id)
                            response_data = {
                                'vle_id': vle_id,
                                'status': '00',
                                'message': "OTP sent successfully",
                            }
                            return Response(response_data, status=status.HTTP_200_OK)
                        else:
                            response_data = {
                                'status': '01',
                                'message': "Failed to send OTP to the user",

                            }
                            return Response(response_data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            if isinstance(e.__cause__, psycopg2.errors.UniqueViolation):
                response_data = {
                    'status': '01',
                    'message': "Provided mobile number already exists with another VLE",

                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                response_data = {
                    'status': '01',
                    'message': "Error occurred while making the request.",

                }
                return Response(response_data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Error occurred while making the request.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleValidateOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        mobile_no = request.data.get('mobile_no')
        otp_code = request.data.get('otp_code')
        vle_id = request.data.get('vle_id')
        primary_or_secondary = request.data.get('primary_or_secondary')
        if primary_or_secondary:
            if VleOtp.objects.filter(mobile_no=mobile_no).exists():
                if VleOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code).exists():
                    response_data = {
                        'status': '00',
                        'message': "OTP verified successfully",
                        'vle_id': vle_id
                    }
                    if primary_or_secondary == 1:
                        VleMobileNumber.objects.filter(vle_id_id=vle_id).update(status="Verified")
                    elif primary_or_secondary == -1:
                        primary_exists = VleMobileNumber.objects.filter(vle_id_id=vle_id).first()
                        if not primary_exists:
                            # return Response({'error': 'Primary Mobile Number Does Not Exist.'},
                            #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            response_data = {
                                'status': '01',
                                'message': "Primary Mobile Number Does Not Exist.",

                            }
                            return Response(response_data, status=status.HTTP_200_OK)
                        elif primary_exists:
                            alternative_numbers_column = primary_exists.alternative_mobile_numbers
                            if isinstance(alternative_numbers_column, list) and not alternative_numbers_column:
                                # return Response({'error': 'Alternate Number Not Found.'},
                                #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                response_data = {
                                    'status': '01',
                                    'message': "Alternate Number Not Found.",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                            elif alternative_numbers_column and isinstance(alternative_numbers_column, list):
                                updated = False
                                for number_entry in alternative_numbers_column:
                                    if (number_entry['alternate_mobile_number'] == mobile_no and
                                            number_entry['alternate_status'] == "Not Verified"):
                                        number_entry['alternate_status'] = "Verified"
                                        updated = True
                                if updated:
                                    primary_exists.save()
                                else:
                                    # return Response({'error': 'Alternate Number Not Found.'},
                                    #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                    response_data = {
                                        'status': '01',
                                        'message': "Alternate Number Not Found.",

                                    }
                                    return Response(response_data, status=status.HTTP_200_OK)
                            else:
                                response_data = {
                                    'status': '01',
                                    'message': "Alternate Number Not Found.",

                                }
                                return Response(response_data, status=status.HTTP_200_OK)
                                # return Response({'error': 'Alternate Number Not Found'},
                                #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return Response(response_data, status=200)
                else:
                    response_data = {
                        'status': '01',
                        'message': "Invalid OTP",
                    }
                    return JsonResponse(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'status': '01',
                    'message': "Mobile number does not exist, Please Resend OTP.",
                }
                return JsonResponse(response_data, status=status.HTTP_200_OK)
            # else:
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if VleOtp.objects.filter(mobile_no=mobile_no).exists():

                if VleOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code).exists():
                    response_data = {
                        'status': '00',
                        'message': "OTP verified successfully",
                        'vle_id': vle_id
                    }
                    # VleMobileNumber.objects.filter(vle_id=vle_id).update(status="Verified")
                    return Response(response_data, status=200)

                else:
                    response_data = {
                        'status': '01',
                        'message': "Invalid OTP",
                    }
                    return JsonResponse(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'status': '01',
                    'message': "Mobile number does not exist, Please Resend OTP.",
                }
                return JsonResponse(response_data, status=status.HTTP_200_OK)

class CheckVLEDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if not vle_id:
                raise ValueError("VLE ID is not provided")

            # tables_with_data = []
            # tables_without_data = []

            models = [VleVillageInfo, BmcBasicInformation, VleBasicInformation, VleMobileNumber, PhotoOfBmc, VLEBankDetails, SkillsAndKnowledge, VLEEconomicAndSocialStatusInfo, VleNearbyMilkCenterContact, VillageDetails]

            response = {
                'status': '00',
                'message': 'success',
            }

            for model in models:
                if model.objects.filter(vle_id=vle_id).exists():
                    response[model.__name__] = 1
                else:
                    response[model.__name__] = -1

            # response = {
            #     'status': '00',
            #     'message': 'success',
            #     'VleVillageInfo':1
            #     'tables_with_data': tables_with_data,
            #     'tables_without_data': tables_without_data
            # }

            return Response(response, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*------Dashboard API------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------


class GetTargetDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            user_id = request.query_params.get('user_id')
            if not user_id:
                raise ValueError("User ID is not provided")
            else:
                employee_id_queryset = EmployeeDetails.objects.filter(employee_id=user_id)
                if employee_id_queryset.exists():
                    employee_id_queryset = employee_id_queryset.first()
                    employee_id = employee_id_queryset.id
                else:
                    return Response({'status': '01', 'message': f'Target is not set for you. '
                                                                f'Kindly reach-out to your reporting manager.',
                                     'week_flag': -1, 'month_flag': -1}, status=status.HTTP_200_OK)

            response = {
                'status': '00',
                'message': 'success',
                'week_flag': 1,
                'month_flag': 1,
                'month_data': [{"loginTarget": "", "visitTarget": "", "disbursementTarget": "",
                                "loginAchieved": "", "visitAchieved": "", "disbursementAchieved": "",
                                "MonthName": "", "MonthId": ""}],
                'current_week_data': [{"loginTarget": "", "visitTarget": "", "disbursementTarget": "",
                                       "loginAchieved": "", "visitAchieved": "", "disbursementAchieved": "",
                                       "weekName": "", "weekId": ""}]
            }
            today_date = date.today()
            month_id = today_date.month
            month = today_date.strftime("%B")
            year = today_date.year
            month_target = EmployeeSetTargetDetails.objects.filter(employee_id=employee_id, month_name=month, year=str(year))
            if not month_target.exists():
                return Response({'status': '01', 'message': f'Target is not set for you. '
                                                            f'Kindly reach-out to your reporting manager.',
                                 'week_flag': -1, 'month_flag': -1}, status=status.HTTP_200_OK)
            elif month_target.exists():
                sum_of_targets = month_target.aggregate(
                    visit_target_sum=Sum('visit_target'),
                    login_target_sum=Sum('login_target'),
                    disbursement_target_sum=Sum('disbursement_target')
                )
                visit_target_sum = sum_of_targets['visit_target_sum']
                login_target_sum = sum_of_targets['login_target_sum']
                disbursement_target_sum = sum_of_targets['disbursement_target_sum']
                response['month_data'][0]['loginTarget'] = str(login_target_sum)
                response['month_data'][0]['visitTarget'] = str(visit_target_sum)
                response['month_data'][0]['disbursementTarget'] = str(disbursement_target_sum)
                response['month_data'][0]['MonthName'] = month
                response['month_data'][0]['MonthId'] = str(month_id)
                week_details = WeekDetails.objects.filter(month_name=month, year=str(year))
                if not week_details.exists():
                    response['week_flag'] = -1
                    response['month_data'][0]['loginAchieved'] = "0"
                    response['month_data'][0]['visitAchieved'] = "0"
                    response['month_data'][0]['disbursementAchieved'] = "0"
                    return Response(response, status=status.HTTP_200_OK)
                elif week_details.exists():
                    week_ids = list(week_details.values_list('id', flat=True))
                    aggregate_visit = 0
                    aggregate_login = 0
                    aggregate_disbursement = 0
                    current_week_details = WeekDetails.objects.filter(start_date__lte=today_date,
                                                                      end_date__gte=today_date)
                    if not current_week_details.exists():
                        response['week_flag'] = -1
                        for week_id in week_ids:
                            week_detail = WeekDetails.objects.get(id=week_id)
                            start_date = week_detail.start_date
                            end_date = week_detail.end_date
                            filtered_data = EmployeeTargetDetails.objects.filter(employee_id=employee_id,
                                                                                 date__range=(start_date, end_date))
                            if not filtered_data.exists():
                                pass
                            elif filtered_data.exists():
                                filtered_data = EmployeeTargetDetails.objects.filter(
                                    employee_id=employee_id,
                                    date__range=(start_date, end_date),
                                    version=Subquery(
                                        EmployeeTargetDetails.objects.filter(
                                            employee_id=OuterRef('employee_id'),
                                            date=OuterRef('date')
                                        ).values('version').order_by('-version').values('version')[:1]
                                    )
                                )
                                total_sums = filtered_data.aggregate(
                                    total_login_achieved=Sum('login_achieved'),
                                    total_visit_achieved=Sum('visit_achieved'),
                                    total_disbursement_achieved=Sum('disbursement_achieved')
                                )
                                total_visit_achieved = total_sums['total_visit_achieved']
                                total_login_achieved = total_sums['total_login_achieved']
                                total_disbursement_achieved = total_sums['total_disbursement_achieved']

                                aggregate_visit += total_visit_achieved
                                aggregate_login += total_login_achieved
                                aggregate_disbursement += total_disbursement_achieved
                        response['month_data'][0]['loginAchieved'] = str(aggregate_login)
                        response['month_data'][0]['visitAchieved'] = str(aggregate_visit)
                        response['month_data'][0]['disbursementAchieved'] = str(aggregate_disbursement)
                        return Response(response, status=status.HTTP_200_OK)
                    elif current_week_details.exists():
                        current_week_details = current_week_details.first()
                        current_week_name = current_week_details.week_name
                        current_week_id = current_week_details.id
                        start_date = current_week_details.start_date
                        end_date = current_week_details.end_date
                        is_current_week_target_set = EmployeeSetTargetDetails.objects.filter(
                            employee_id=employee_id, month_name=month, year=str(year), week_id=current_week_id)
                        if not is_current_week_target_set.exists():
                            response['week_flag'] = -1
                            remaining_week_list = [week for week in week_ids if week != current_week_id]
                            if remaining_week_list:
                                for week_id in remaining_week_list:
                                    week_detail = WeekDetails.objects.get(id=week_id)
                                    start_date = week_detail.start_date
                                    end_date = week_detail.end_date
                                    filtered_data = EmployeeTargetDetails.objects.filter(employee_id=employee_id,
                                                                                         date__range=(start_date, end_date))
                                    if not filtered_data.exists():
                                        pass
                                    elif filtered_data.exists():
                                        filtered_data = EmployeeTargetDetails.objects.filter(
                                            employee_id=employee_id,
                                            date__range=(start_date, end_date),
                                            version=Subquery(
                                                EmployeeTargetDetails.objects.filter(
                                                    employee_id=OuterRef('employee_id'),
                                                    date=OuterRef('date')
                                                ).values('version').order_by('-version').values('version')[:1]
                                            )
                                        )
                                        total_sums = filtered_data.aggregate(
                                            total_login_achieved=Sum('login_achieved'),
                                            total_visit_achieved=Sum('visit_achieved'),
                                            total_disbursement_achieved=Sum('disbursement_achieved')
                                        )
                                        total_visit_achieved = total_sums['total_visit_achieved']
                                        total_login_achieved = total_sums['total_login_achieved']
                                        total_disbursement_achieved = total_sums['total_disbursement_achieved']
                                        aggregate_visit += total_visit_achieved
                                        aggregate_login += total_login_achieved
                                        aggregate_disbursement += total_disbursement_achieved
                                response['month_data'][0]['loginAchieved'] = str(aggregate_login)
                                response['month_data'][0]['visitAchieved'] = str(aggregate_visit)
                                response['month_data'][0]['disbursementAchieved'] = str(aggregate_disbursement)
                                return Response(response, status=status.HTTP_200_OK)
                            else:
                                response['month_data'][0]['loginAchieved'] = str(aggregate_login)
                                response['month_data'][0]['visitAchieved'] = str(aggregate_visit)
                                response['month_data'][0]['disbursementAchieved'] = str(aggregate_disbursement)
                                return Response(response, status=status.HTTP_200_OK)
                        else:
                            filtered_data = EmployeeTargetDetails.objects.filter(employee_id=employee_id,
                                                                                 date__range=(start_date, end_date))
                            if not filtered_data.exists():
                                response['current_week_data'][0]['loginAchieved'] = str(aggregate_login)
                                response['current_week_data'][0]['visitAchieved'] = str(aggregate_visit)
                                response['current_week_data'][0]['disbursementAchieved'] = str(aggregate_disbursement)
                                response['current_week_data'][0]['weekName'] = current_week_name
                                response['current_week_data'][0]['weekId'] = str(current_week_id)
                                current_week_set_target = EmployeeSetTargetDetails.objects.filter(
                                    employee_id=employee_id, month_name=month, year=str(year), week_id=current_week_id).first()
                                response['current_week_data'][0]['loginTarget'] = str(current_week_set_target.login_target)
                                response['current_week_data'][0]['visitTarget'] = str(current_week_set_target.visit_target)
                                response['current_week_data'][0]['disbursementTarget'] = str(current_week_set_target.disbursement_target)
                            elif filtered_data.exists():
                                filtered_data = EmployeeTargetDetails.objects.filter(
                                    employee_id=employee_id,
                                    date__range=(start_date, end_date),
                                    version=Subquery(
                                        EmployeeTargetDetails.objects.filter(
                                            employee_id=OuterRef('employee_id'),
                                            date=OuterRef('date')
                                        ).values('version').order_by('-version').values('version')[:1]
                                    )
                                )
                                current_total_sums = filtered_data.aggregate(
                                    total_login_achieved=Sum('login_achieved'),
                                    total_visit_achieved=Sum('visit_achieved'),
                                    total_disbursement_achieved=Sum('disbursement_achieved')
                                )
                                current_total_visit_achieved = current_total_sums['total_visit_achieved']
                                current_total_login_achieved = current_total_sums['total_login_achieved']
                                current_total_disbursement_achieved = current_total_sums['total_disbursement_achieved']

                                response['current_week_data'][0]['loginAchieved'] = str(current_total_login_achieved)
                                response['current_week_data'][0]['visitAchieved'] = str(current_total_visit_achieved)
                                response['current_week_data'][0]['disbursementAchieved'] = str(current_total_disbursement_achieved)
                                response['current_week_data'][0]['weekName'] = current_week_name
                                response['current_week_data'][0]['weekId'] = str(current_week_id)
                                aggregate_visit += current_total_visit_achieved
                                aggregate_login += current_total_login_achieved
                                aggregate_disbursement += current_total_disbursement_achieved
                                current_week_set_target = EmployeeSetTargetDetails.objects.filter(
                                    employee_id=employee_id, month_name=month, year=str(year), week_id=current_week_id).first()
                                response['current_week_data'][0]['loginTarget'] = str(current_week_set_target.login_target)
                                response['current_week_data'][0]['visitTarget'] = str(current_week_set_target.visit_target)
                                response['current_week_data'][0]['disbursementTarget'] = str(current_week_set_target.disbursement_target)
                            remaining_week_list = [week for week in week_ids if week != current_week_id]
                            if remaining_week_list:
                                for week_id in remaining_week_list:
                                    week_detail = WeekDetails.objects.get(id=week_id)
                                    start_date = week_detail.start_date
                                    end_date = week_detail.end_date
                                    filtered_data = EmployeeTargetDetails.objects.filter(employee_id=employee_id,
                                                                                         date__range=(start_date, end_date))
                                    if not filtered_data.exists():
                                        pass
                                    elif filtered_data.exists():
                                        filtered_data = EmployeeTargetDetails.objects.filter(
                                            employee_id=employee_id,
                                            date__range=(start_date, end_date),
                                            version=Subquery(
                                                EmployeeTargetDetails.objects.filter(
                                                    employee_id=OuterRef('employee_id'),
                                                    date=OuterRef('date')
                                                ).values('version').order_by('-version').values('version')[:1]
                                            )
                                        )
                                        total_sums = filtered_data.aggregate(
                                            total_login_achieved=Sum('login_achieved'),
                                            total_visit_achieved=Sum('visit_achieved'),
                                            total_disbursement_achieved=Sum('disbursement_achieved')
                                        )
                                        total_visit_achieved = total_sums['total_visit_achieved']
                                        total_login_achieved = total_sums['total_login_achieved']
                                        total_disbursement_achieved = total_sums['total_disbursement_achieved']

                                        aggregate_visit += total_visit_achieved
                                        aggregate_login += total_login_achieved
                                        aggregate_disbursement += total_disbursement_achieved
                                response['month_data'][0]['loginAchieved'] = str(aggregate_login)
                                response['month_data'][0]['visitAchieved'] = str(aggregate_visit)
                                response['month_data'][0]['disbursementAchieved'] = str(aggregate_disbursement)
                                return Response(response, status=status.HTTP_200_OK)
                            else:
                                response['month_data'][0]['loginAchieved'] = str(aggregate_login)
                                response['month_data'][0]['visitAchieved'] = str(aggregate_visit)
                                response['month_data'][0]['disbursementAchieved'] = str(aggregate_disbursement)
                                return Response(response, status=status.HTTP_200_OK)
                    return Response(response, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -----------------------------------*------Privacy Policy Webpage------*--------------------------------------*--------

def privacy_policy(request):
    return render(request, 'privacy-policy.html')




class CustomAPIException(APIException):
    status_code = 400
    default_detail = 'A server error occurred.'
    default_code = 'error'

# -----------------------------------*------------Query API-------------*--------------------------------------*--------
class QueryDataView(APIView):
    permission_classes = [AllowAny]

    def get_max_version_queries(self, cluster_head_id=None, selected_rm_id=None, selected_so_id=None):

        base_filter = Q()

        if cluster_head_id:
            base_filter &= Q(
                saswat_application_number__sales_officer__reporting_manager__cluster_head_id=cluster_head_id) | \
                           Q(saswat_application_number__sales_officer__cluster_head_id=cluster_head_id)

        if selected_rm_id:
            base_filter &= Q(saswat_application_number__sales_officer__reporting_manager_id=selected_rm_id)

        if selected_so_id:
            base_filter &= Q(saswat_application_number__sales_officer_id=selected_so_id)

        # Subquery to get the max version of each query_id
        subquery = QueryModel.objects.filter(
            base_filter
        ).values('query_id').annotate(
            max_version=Max('version')
        ).values('query_id', 'max_version')

        # Main query to get the latest version query data
        latest_queries = QueryModel.objects.filter(
            base_filter,
            version=Subquery(subquery.values('max_version').filter(query_id=OuterRef('query_id')))
        )

        return latest_queries

    # def get_latest_queries(self, query_id=None, saswat_application_numbers=None, query_status=None):
    #     base_queryset = QueryModel.objects.filter(
    #         saswat_application_number__saswat_application_number__in=saswat_application_numbers,
    #     )
    #
    #     latest_version_subquery = QueryModel.objects.filter(
    #         query_id=OuterRef('query_id'),
    #         saswat_application_number__saswat_application_number__in=saswat_application_numbers
    #     ).values('query_id').annotate(
    #         latest_version=Max('version')
    #     ).values('latest_version')
    #
    #     if query_status:
    #         if query_status.upper() == "OPEN":
    #             queryset = base_queryset.filter(
    #                 Q(query_status="OPEN") | Q(query_status="REOPENED"),
    #                 version=Subquery(latest_version_subquery)
    #             )
    #         else:
    #             queryset = base_queryset.filter(
    #                 query_status=query_status.upper(),
    #                 version=Subquery(latest_version_subquery)
    #             )
    #     else:
    #         queryset = base_queryset.filter(
    #             version=Subquery(latest_version_subquery)
    #         )
    #
    #     if query_id:
    #         queryset = queryset.filter(query_id=query_id)
    #
    #     return queryset

    def get_latest_queries(self, query_id=None, saswat_application_numbers=None, query_status=None):
        # Base queryset with saswat_application_numbers filter
        base_queryset = QueryModel.objects.filter(
            saswat_application_number__saswat_application_number__in=saswat_application_numbers,
        )

        # Subquery to get the maximum version for each query_id
        max_version_subquery = QueryModel.objects.filter(
            query_id=OuterRef('query_id')
        ).values('query_id').annotate(
            max_version=Max('version')
        ).values('max_version')

        # Filter to get only the latest version for each query_id
        queryset = base_queryset.filter(
            version=Subquery(max_version_subquery)
        )

        # Handle query_status filter with special case for 'OPEN'
        if query_status:
            query_status_upper = query_status.upper()

            if query_status_upper == "OPEN":
                # Annotate queryset to handle cases where the max version has status 'DRAFT'
                queryset = queryset.annotate(
                    adjusted_status=Case(
                        When(query_status="DRAFT", then=Value("OPEN")),
                        default=F('query_status'),
                        output_field=CharField()
                    )
                ).filter(adjusted_status="OPEN")
            else:
                # Apply other status filters directly
                queryset = queryset.filter(query_status=query_status_upper)

        # Apply additional filtering by query_id if provided
        if query_id:
            queryset = queryset.filter(query_id=query_id)

        return queryset

    def serialize_and_respond(self, queryset, attachment_queryset, status_code=status.HTTP_200_OK):
        if queryset.exists():
            query_serializer = GetQuerySerializer(queryset, many=True)
            for query_data in query_serializer.data:
                if query_data['query_status'] == "DRAFT":
                    query_data['query_status'] = "OPEN"
            attachment_serializer = QnaAttachmentSerializer(attachment_queryset, many=True)
            return Response({
                'status': '00',
                'message': 'success',
                'status_counts': [],
                'relationship_managers': [],
                'sales_officers': [],
                'queries': query_serializer.data,
                'attachments': attachment_serializer.data,
            }, status=status_code)
        return Response({'status': '01', 'message': 'No Records found.'}, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        try:
            user_id = request.query_params.get('user_id')
            query_id = request.query_params.get('query_id')
            row_id = request.query_params.get('row_id')
            param_status = request.query_params.get('status')
            selected_rm_id = request.query_params.get('selected_rm_id')
            selected_so_id = request.query_params.get('selected_so_id')


            if not user_id:
                raise CustomAPIException("User ID is not provided")

            query_status = param_status.upper() if param_status else None

            employee = EmployeeDetails.objects.filter(employee__user_id=user_id).first()
            if not employee:
                return Response({'status': '01', 'message': 'No Loan Applications found for the given user.'},
                                status=status.HTTP_200_OK)

            response_data = {'status': '00'}

            all_statuses = ['OPEN', 'REOPENED', 'ANSWERED', 'VERIFIED']

            def get_status_counts(latest_queries):
                status_counts = latest_queries.values('query_status').annotate(count=Count('query_status'))
                status_counts_dict = {status: 0 for status in all_statuses}
                for status in status_counts:
                    status_counts_dict[status['query_status']] = status['count']
                return status_counts_dict

            # Cluster Head logic
            if employee.designation.designation_name == 'Cluster Head':
                if selected_so_id:
                    # If an SO is selected, show their loan applications
                    loan_applications = LoanApplication.objects.filter(sales_officer=selected_so_id)

                    if not loan_applications.exists():
                        return Response(
                            {
                                'status': '01',
                                'message': 'No Loan Applications found for the selected Sales Officer.'
                            },
                            status=status.HTTP_200_OK)

                    serializer = LoanApplicationSerializer(loan_applications, many=True)
                    saswat_application_numbers = [app['saswat_application_number'] for app in serializer.data]

                    query_data = self.get_latest_queries(query_id, saswat_application_numbers, query_status)


                    attachment_queryset = QnaAttachment.objects.none()
                    if query_id:
                        attachment_queryset = QnaAttachment.objects.filter(query_id=row_id)

                    return self.serialize_and_respond(query_data, attachment_queryset)

                elif selected_rm_id:
                    # If an RM is selected, show SOs under this RM

                    relationship_manager = get_object_or_404(EmployeeDetails, id=selected_rm_id)
                    emp = [relationship_manager]

                    sales_officers = EmployeeDetails.objects.filter(reporting_manager=relationship_manager)
                    combined_sales_officers = emp + list(sales_officers)
                    so_serializer = EmployeeDetailsSerializer(combined_sales_officers, many=True)

                    latest_queries = self.get_max_version_queries(employee.id, selected_rm_id=selected_rm_id)
                    status_counts_dict = get_status_counts(latest_queries)
                    status_counts_dict = [status_counts_dict]


                    response_data.update( {
                        'status': '00',
                        'message': 'success',
                        'status_counts': status_counts_dict,
                        'relationship_managers': [],
                        'sales_officers': so_serializer.data,
                        'queries': [],
                        'attachments': []
                    })
                    return Response(response_data, status=status.HTTP_200_OK)

                else:
                    # If no RM is selected, show RMs under the cluster head
                    # relationship_managers = EmployeeDetails.objects.filter(cluster_head=employee)
                    relationship_managers = EmployeeDetails.objects.filter(
                        cluster_head=employee
                    ).exclude(
                        ~Q(reporting_manager__isnull=True)
                    )
                    rm_serializer = EmployeeDetailsSerializer(relationship_managers, many=True)
                    data = rm_serializer.data
                    rm_data = [item for item in data if item['designation'] == 2]
                    so_data = [item for item in data if item['designation'] == 3]

                    latest_queries = self.get_max_version_queries(employee.id)
                    status_counts_dict = get_status_counts(latest_queries)
                    status_counts_dict = [status_counts_dict]


                    response_data.update( {
                        'status': '00',
                        'message': 'success',
                        'status_counts': status_counts_dict,
                        'relationship_managers': rm_data,
                        'sales_officers': so_data,
                        'queries': [],
                        'attachments': []


                    })
                    return Response(response_data, status=status.HTTP_200_OK)

            elif employee.designation.designation_name == 'Reporting Manager':

                if selected_so_id:
                    # If an SO is selected, show their loan applications
                    loan_applications = LoanApplication.objects.filter(sales_officer=selected_so_id)

                    if not loan_applications.exists():
                        return Response(
                            {'status': '01', 'message': 'No Loan Applications found for the selected Sales Officer.'},
                            status=status.HTTP_200_OK)

                    serializer = LoanApplicationSerializer(loan_applications, many=True)
                    saswat_application_numbers = [app['saswat_application_number'] for app in serializer.data]

                    query_data = self.get_latest_queries(query_id, saswat_application_numbers, query_status)

                    attachment_queryset = QnaAttachment.objects.none()
                    if query_id:
                        attachment_queryset = QnaAttachment.objects.filter(query_id=row_id)

                    return self.serialize_and_respond(query_data, attachment_queryset)

                else:
                    # If no SO is selected, show SOs under the reporting manager

                    emp = [employee]
                    sales_officers = EmployeeDetails.objects.filter(reporting_manager=employee)
                    combined_sales_officers = emp + list(sales_officers)
                    so_serializer = EmployeeDetailsSerializer(combined_sales_officers, many=True)
                    data = so_serializer.data
                    rm_data = [item for item in data if item['designation'] == 2]
                    so_data = [item for item in data if item['designation'] == 3 or item['designation'] == 2]


                    latest_queries = self.get_max_version_queries(selected_rm_id=employee.id)
                    status_counts_dict = get_status_counts(latest_queries)
                    status_counts_dict = [status_counts_dict]



                    response_data.update( {
                        'status': '00',
                        'message': 'success',
                        'status_counts': status_counts_dict,
                        'relationship_managers':[],
                        'sales_officers': so_data,
                        'queries': [],
                        'attachments': []
                    })
                    return Response(response_data, status=status.HTTP_200_OK)

            # Sales Officer logic
            elif employee.designation.designation_name == 'Sales Officer':
                loan_applications = LoanApplication.objects.filter(sales_officer=employee.id)
                latest_queries = self.get_max_version_queries(selected_so_id=employee.id)
                status_counts_dict = get_status_counts(latest_queries)

                if not loan_applications.exists():
                    return Response({'status': '01', 'message': 'No Loan Applications found for the given user.'},
                                    status=status.HTTP_200_OK)

                serializer = LoanApplicationSerializer(loan_applications, many=True)
                saswat_application_numbers = [app['saswat_application_number'] for app in serializer.data]

                query_data = self.get_latest_queries(query_id, saswat_application_numbers, query_status)

                attachment_queryset = QnaAttachment.objects.none()
                if query_id:
                    attachment_queryset = QnaAttachment.objects.filter(query_id=row_id)

                return self.serialize_and_respond(query_data, attachment_queryset)

            else:
                # For other designations, no loan applications will be shown
                return Response({'status': '01', 'message': 'No Loan Applications found for the given user.'},
                                status=status.HTTP_200_OK)
        except CustomAPIException as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            q_id = request.data.get('id')
            saswat_application_number = request.data.get('saswat_application_number')
            query_id = request.data.get('query_id')
            if not q_id or not saswat_application_number:
                raise CustomAPIException("ID or Saswat Application Number is not provided")
            query_data_queryset = QueryModel.objects.filter(id=q_id)
            if not query_data_queryset.exists():
                return Response({'status': '01', 'message': f'No Queries found for the given '
                                                            f'Saswat Application Number.'},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                existing_entries_count = QueryModel.objects.filter(query_id=query_id).count() + 1
                serializer = NewQuerySerializer(data=request.data,
                                                context={'request': request, 'version': existing_entries_count,
                                                         'query_id': query_id})

                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status': '00',
                        'message': 'Query created/updated successfully',
                        'data': serializer.data
                    }, status=status.HTTP_201_CREATED)
                return Response({
                    'status': '01',
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except CustomAPIException as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            q_id = request.data.get('id')
            query_status = request.data.get('query_status')

            if not q_id:
                raise CustomAPIException("ID is not provided.")
            if not query_status:
                raise CustomAPIException("Query status is not provided.")

            # Retrieve the query instance
            query_instance = QueryModel.objects.filter(id=q_id).first()

            if not query_instance:
                return Response({'status': '01', 'message': 'Query not found.'},
                                status=status.HTTP_200_OK)

            # Partial update to only modify the query_status field
            serializer = QueryStatusUpdateSerializer(query_instance, data={'query_status': query_status}, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': '00',
                    'message': 'Query status updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': '01',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_200_OK)

        except CustomAPIException as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def get_latest_queries(self, query_id=None, saswat_application_numbers=None, query_status=None):
    #     base_queryset = QueryModel.objects.filter(
    #         saswat_application_number__saswat_application_number__in=saswat_application_numbers,
    #     )
    #
    #     latest_version_subquery = QueryModel.objects.filter(
    #         query_id=OuterRef('query_id'),
    #         saswat_application_number__saswat_application_number__in=saswat_application_numbers
    #     ).values('query_id').annotate(
    #         latest_version=Max('version')
    #     ).values('latest_version')
    #
    #     if query_status:
    #         if query_status.upper() == "OPEN":
    #             queryset = base_queryset.filter(
    #                 Q(query_status="OPEN") | Q(query_status="REOPENED"),
    #                 version=Subquery(latest_version_subquery)
    #             )
    #         else:
    #             queryset = base_queryset.filter(
    #                 query_status=query_status.upper(),
    #                 version=Subquery(latest_version_subquery)
    #             )
    #     else:
    #         queryset = base_queryset.filter(
    #             version=Subquery(latest_version_subquery)
    #         )
    #
    #     if query_id:
    #         queryset = queryset.filter(query_id=query_id)
    #
    #     return queryset
    # def serialize_and_respond(self, queryset, attachment_queryset, status_code=status.HTTP_200_OK):
    #     if queryset.exists():
    #         query_serializer = GetQuerySerializer(queryset, many=True)
    #         attachment_serializer = QnaAttachmentSerializer(attachment_queryset, many=True)
    #         return Response({
    #             'status': '00',
    #             'message': 'success',
    #             'queries': query_serializer.data,
    #             'attachments': attachment_serializer.data
    #         }, status=status_code)
    #     return Response({'status': '01', 'message': 'No Records found.'}, status=status.HTTP_200_OK)
    #
    # def get(self, request, format=None):
    #     try:
    #         user_id = request.query_params.get('user_id')
    #         query_id = request.query_params.get('query_id')
    #         row_id = request.query_params.get('row_id')
    #         param_status = request.query_params.get('status')
    #
    #         if not user_id:
    #             raise CustomAPIException("User ID is not provided")
    #
    #         query_status = param_status.upper() if param_status else None
    #
    #         employee = EmployeeDetails.objects.filter(employee_id=user_id).first()
    #         if not employee:
    #             return Response({'status': '01', 'message': 'No Loan Applications found for the given user.'},
    #                             status=status.HTTP_200_OK)
    #
    #         loan_applications = LoanApplication.objects.filter(sales_officer=employee.id)
    #         if not loan_applications.exists():
    #             return Response({'status': '01', 'message': 'No Loan Applications found for the given user.'},
    #                             status=status.HTTP_200_OK)
    #
    #         serializer = LoanApplicationSerializer(loan_applications, many=True)
    #         saswat_application_numbers = [app['saswat_application_number'] for app in serializer.data]
    #
    #         query_data = self.get_latest_queries(query_id, saswat_application_numbers, query_status)
    #
    #         attachment_queryset = QnaAttachment.objects.none()
    #         if query_id:
    #             attachment_queryset = QnaAttachment.objects.filter(query=row_id)
    #
    #         return self.serialize_and_respond(query_data, attachment_queryset)
    #
    #     except CustomAPIException as e:
    #         return Response({'status': '01', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SoAndTaAttachmentAPIView(APIView):

    def get(self, request):
        try:
            attachments = QnaAttachment.objects.all()
            serializer = QnaAttachmentSerializer(attachments, many=True)
            return Response({'status': '00', 'message': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = QnaAttachmentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': '00', 'message': 'Attachment created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except CustomAPIException as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class SignInSignOutView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         signin_signout_serializer = SignInSignOutSerializer(data=request.data)
#         try:
#             if signin_signout_serializer.is_valid():
#                 signin_signout_serializer.save()
#                 response_data = {
#                     'status': '00',
#                     'message': "success",
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
#             else:
#                 return Response(signin_signout_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignInSignOutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        signin_signout_serializer = SignInSignOutSerializer(data=request.data)
        try:
            if signin_signout_serializer.is_valid():
                signin_signout_serializer.save()
                response_data = {
                    'status': '00',
                    'message': "success",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            elif "remarks_one" in signin_signout_serializer.errors:
                if ("Not a valid string." in signin_signout_serializer.errors["remarks_one"] and
                        isinstance(signin_signout_serializer.data['remarks_one'], dict)):
                    user_id = signin_signout_serializer.data['user']
                    client_id = signin_signout_serializer.data['client_id']
                    event_type = signin_signout_serializer.data['event_type']
                    event_date = signin_signout_serializer.data['event_date']
                    event_time = signin_signout_serializer.data['event_time']
                    remarks_one_dump = json.dumps(signin_signout_serializer.data['remarks_one'])
                    SignInSignOut.objects.create(user_id=user_id, client_id=client_id, event_type=event_type,
                                                 event_date=event_date, event_time=event_time,
                                                 remarks_one=remarks_one_dump)
                    response_data = {
                        'status': '00',
                        'message': "success",
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                return Response(signin_signout_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(signin_signout_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_shortened_query_details(request, pk):
    try:
        shortened_query = ShortenedQueries.objects.get(pk=pk)
        data = {
            'description': shortened_query.description,
            'additional_info': shortened_query.additional_info,
        }
    except ShortenedQueries.DoesNotExist:
        data = {
            'description': '',
            'additional_info': '',
        }
    return JsonResponse(data)

def get_documents(request, document_id):
    shortened_queries = ShortenedQueries.objects.filter(document__id=document_id).values('id', 'shortened_query')
    return JsonResponse({'shortened_queries': list(shortened_queries)})


class GetESIgnView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.query_params.get('user_id')
            if not user_id:
                raise ValueError("User ID is not provided.")
            query_set = ESign.objects.filter(user_id=user_id)
            if not query_set.exists():
                response_data = {
                    'status': '01',
                    'message': 'No Data Found.'
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                serializer = ESignSerializer(query_set, many=True)
                response_data = {
                    'status': '00',
                    'message': 'Success.',
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ESignView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            customer_mobile_number = request.data.get('customer_mobile_number')
            customer_name = request.data.get('customer_name')
            file_name = request.data.get('file_name')
            file_data_base64 = request.data.get('file_data_base64')
            file = request.FILES.get('file')
            created_by = request.data.get('created_by')
            modified_by = request.data.get('modified_by')
            if not user_id:
                raise ValueError("User ID is not provided.")
            if not customer_mobile_number:
                raise ValueError("Customer Mobile Number is not provided.")
            if not customer_name:
                raise ValueError("Customer Name is not provided.")
            if not file_name:
                raise ValueError("File Name is not provided.")
            if not file_data_base64:
                raise ValueError("Base 64 Data of File is not provided.")
            if not file:
                raise ValueError("File is not provided.")
            if not created_by:
                raise ValueError("'Created By' is not provided.")
            if not modified_by:
                raise ValueError("'Modified By' is not provided.")
            validate_login_url = 'http://98.70.76.243:8083/saswat/validate_login'
            username = "pooja@saswatfinance.com"
            password = "javaBOOK26*"
            validate_request_data = {
                'UserName': username,
                'Password': password
            }
            try:
                response = requests.post(validate_login_url, json=validate_request_data)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                if response is None or not response.content:
                    response_data = {
                        'status': '01',
                        'message': 'No Response received, Please try again.'
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                elif (response and response.status_code == 200 and
                      response.headers.get('content-type') == 'application/json'):
                    try:
                        response_content = response.json()  # Attempt to parse JSON
                    except ValueError:
                        response_data = {
                            'status': '01',
                            'message': 'Some error occurred, Please try again.'
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        'status': '01',
                        'message': 'Some error occurred, Please try again.'
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
            except requests.exceptions.HTTPError as http_err:
                error_message = f'HTTP error occurred: {http_err}'
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except MaxRetryError as e:
                error_message = f"Max retries exceeded when trying to connect to server. Error: {e}"
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except NewConnectionError as e:
                error_message = f"Failed to establish a new connection: {e}"
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except requests.exceptions.ConnectionError as conn_err:
                error_message = f'Error connecting to the server: {conn_err}'
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except requests.exceptions.Timeout as timeout_err:
                error_message = f'Timeout error occurred: {timeout_err}'
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except requests.exceptions.RequestException as req_err:
                error_message = f'An error occurred: {req_err}'
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            name = "Pooja"
            email = "pooja@saswatfinance.com"
            redirect_url = ""
            signatory_email_ids = ["duke30@yopmail.com", "duke12@yopmail.com"]
            list_document_details = [
                {
                    "DocumentName": str(file_name),
                    "FileData": str(file_data_base64),
                    "ControlDetails": [
                        {
                            "PageNo": 1,
                            "SearchText": "",
                            "ControlID": 4,
                            "Anchor": "Top",
                            "AssignedTo": 1,
                            "Left": 2,
                            "Top": 250,
                            "Height": 190,
                            "Width": 122
                        },
                        {
                            "PageNo": "1",
                            "SearchText": "",
                            "ControlID": 4,
                            "Anchor": "Top",
                            "AssignedTo": 2,
                            "Left": 497,
                            "Top": 250,
                            "Height": 438,
                            "Width": 515
                        }
                    ]
                }
            ]
            embedded_signing_url = 'http://98.70.76.243:8083/saswat/initiate_embedded_signing'
            request_data = {
                'Name': name,
                'EmailId': email,
                'RedirectURL': redirect_url,
                'SignatoryEmailIds': signatory_email_ids,
                'lstDocumentDetails': list_document_details
            }
            try:
                auth_token_status = response_content['IsSuccess']
                if not auth_token_status:
                    response_data = {
                        'status': '01',
                        'message': 'Auth Token not generated, Please try again.'
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                response = requests.post(embedded_signing_url, json=request_data)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                if response is None or not response.content:
                    response_data = {
                        'status': '01',
                        'message': 'No Response received, Please try again.'
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                if (response and response.status_code == 200 and
                        response.headers.get('content-type') == 'application/json'):
                    try:
                        response_content_final = response.json()  # Attempt to parse JSON
                        if response_content_final['status'] and response_content_final['status'] == "true":
                            query_set = ESign.objects.create(user_id=user_id,
                                                             customer_mobile_number=str(customer_mobile_number),
                                                             customer_name=str(customer_name), file_name=str(file_name),
                                                             file=file, file_data_base64=str(file_data_base64),
                                                             validate_login_api_response=response_content,
                                                             embedded_signing_api_response=response_content_final,
                                                             esign_status='Link Sent',
                                                             created_by=str(created_by), modified_by=str(modified_by))
                            response_data = {
                                'status': '00',
                                'message': 'URL to sign the document has been sent.',
                                'response': response_content_final
                            }
                            return Response(response_data, status=status.HTTP_200_OK)
                        else:
                            response_data = {
                                'status': '01',
                                'message': 'Some error occurred, Please try again.'
                            }
                            return Response(response_data, status=status.HTTP_200_OK)
                    except ValueError:
                        response_data = {
                            'status': '01',
                            'message': 'Some error occurred, Please try again.'
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        'status': '01',
                        'message': 'Some error occurred, Please try again.'
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
            except requests.exceptions.HTTPError as http_err:
                error_message = f'HTTP error occurred: {http_err}'
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except MaxRetryError as e:
                error_message = f"Max retries exceeded when trying to connect to server. Error: {e}"
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except NewConnectionError as e:
                error_message = f"Failed to establish a new connection: {e}"
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except requests.exceptions.ConnectionError as conn_err:
                error_message = f'Error connecting to the server: {conn_err}'
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except requests.exceptions.Timeout as timeout_err:
                error_message = f'Timeout error occurred: {timeout_err}'
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except requests.exceptions.RequestException as req_err:
                error_message = f'An error occurred: {req_err}'
                response_data = {
                    'status': '01',
                    'message': error_message
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            row_id = request.data.get('id')
            if not row_id:
                raise ValueError("ID is not provided")
            query_data_queryset = ESign.objects.filter(id=row_id)
            if not query_data_queryset.exists():
                return Response({'status': '01', 'message': f'No matching record found.'},
                                status=status.HTTP_200_OK)
            else:
                query_data_queryset = query_data_queryset.first()
                serializer = ESignSerializer(query_data_queryset, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': '01', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)