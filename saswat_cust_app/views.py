# import string
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
# from django.shortcuts import get_object_or_404
# from .utils import is_valid_indian_mobile_number
from rest_framework.exceptions import ValidationError
from saswat_cust_app.models import (UserOtp, UserDetails, CustomerTest, Gender, State, VleVillageInfo,
                                    VleBasicInformation, VleMobileNumber, BmcBasicInformation, VLEBankDetails,
                                    VillageDetails, VleNearbyMilkCenterContact, VLEEconomicAndSocialStatusInfo,
                                    PhotoOfBmc, SkillsAndKnowledge,VleMobileVOtp,VleOtp, Country, District,
                                    DesignationDetails, WeekDetails, EmployeeDetails, EmployeeTargetDetails,
                                    EmployeeSetTargetDetails)

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
                                         VillageDetailsSerializer, VleMobileVOtpSerializer, VleOtpSerializer)
from datetime import datetime, timedelta, date
import requests
# from rest_framework.authentication import SessionAuthentication
from .authenticate import MobileNumberAuthentication
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Sum, Max, OuterRef, Subquery
from django.db import connection
from django.shortcuts import render

class SendOTPAPIView(APIView):

    def post(self, request, *args, **kwargs):
        mobile_no = request.data.get('mobile_no')
        if mobile_no == "8888888888" or mobile_no == 8888888888:
            response_data = {
                'status': '00',
                'message': "OTP sent successfully",

            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:

            url = 'http://ci1.saswatfinance.com:8084/api/otp'
            #url = 'http://20.235.255.141:8084/saswat/otp'
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
            if (mobile_no == "8888888888" or mobile_no == 8888888888) and (otp_code == "1234" or otp_code == 1234):
                if UserDetails.objects.filter(mobile_no=mobile_no).exists():
                    user_det = UserDetails.objects.filter(mobile_no=mobile_no).first()
                    session_id = request.auth
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
                    return Response(response_data, status=200)
                else:
                    response_data = {
                        'status': '01',
                        'message': "Mobile number does not exist",
                    }
                    return JsonResponse(response_data, status=status.HTTP_200_OK)

            else:

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

    def get(self, request, format=None):
        try:
            user_id = request.query_params.get('user_id')
            if not user_id:
                raise ValueError("User ID is not provided")

            village_info_data = VleVillageInfo.objects.filter(user_id=user_id).values('vle_id', 'village_name')
            basic_info_data = VleBasicInformation.objects.filter(user_id=user_id).values('vle_id', 'vle_name')
            common_data = []
            for vle_village_info in village_info_data:
                for vle_basic_info in basic_info_data:
                    if vle_village_info['vle_id'] == vle_basic_info['vle_id']:
                        common_data.append({
                            'vle_id': vle_village_info['vle_id'],
                            'village_name': vle_village_info['village_name'],
                            'vle_name': vle_basic_info['vle_name']
                        })
                    elif vle_village_info['vle_id']:
                        common_data.append({
                            'vle_id': vle_village_info['vle_id'],
                            'village_name': vle_village_info['village_name'],
                            'vle_name': ""
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
        print(vle_v_info_serializer)
        try:
            if vle_v_info_serializer.is_valid():
                vle_id_instance = vle_v_info_serializer.save()
                print(vle_id_instance)
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
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = VleMobileNumberSerializer(mo_no_instance, data=request.data)
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


class PhotoOfBmcView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            vle_id = request.query_params.get('vle_id')
            if vle_id:
                photo_of_bmc_queryset = PhotoOfBmc.objects.filter(vle_id=vle_id)
                if not photo_of_bmc_queryset.exists():
                    return Response({'status': '01', 'msg': 'Data does not exist', 'data': []},
                                    status=status.HTTP_200_OK)
                serializer = PhotoOfBmcSerializer(photo_of_bmc_queryset, many=True)
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
        photo_of_bmc_serializer = PhotoOfBmcSerializer(data=request.data)
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
                return Response(photo_of_bmc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            vle_id = request.data.get('vle_id')
            if vle_id:
                photo_bmc_instance = PhotoOfBmc.objects.filter(vle_id=vle_id).first()
                if not photo_bmc_instance:
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = PhotoOfBmcSerializer(photo_bmc_instance, data=request.data)
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
            if vle_id:
                milk_center_instance = VleNearbyMilkCenterContact.objects.filter(vle_id=vle_id).first()
                if not milk_center_instance:
                    return Response({'error': 'BmcBasicInformation instance not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = VleNearbyMilkCenterContactSerializer(milk_center_instance, data=request.data)
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


class VleMobileVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        vle_mobile_number = request.data.get('mobile_no')
        vle_id = request.data.get('vle_id')
        user_id = request.data.get('user_id')
        url = 'http://ci1.saswatfinance.com:8084/api/otp'

        try:
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
                        data = {
                            'otp': otp_code,
                            'dest': vle_mobile_number,
                                }
                        response = requests.post(url, json=data)
                        print(response)
                        if response.status_code == 200:
                            VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code, vle_id_id=vle_id, user_id=user_id)
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
                            return Response(response_data,
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Optionally, perform additional actions after deletion
                    except Exception as e:
                        print("Error deleting existing OTPs:", e)
                else:
                    print("No existing OTPs found for the provided mobile number.")
                # if existing_otp:
                #     existing_otp.delete()
                #
                # else:
                    existing_otp = VleOtp.objects.filter(vle_id_id=vle_id)
                    if existing_otp.exists():
                        existing_otp.delete()
                    otp_code = str(random.randint(1000, 9999))
                    data = {
                        'otp': otp_code,
                        'dest': vle_mobile_number,
                    }
                    response = requests.post(url, json=data)
                    print(response)
                    if response.status_code == 200:
                        VleOtp.objects.create(mobile_no=str(vle_mobile_number), otp_code=otp_code, vle_id_id=vle_id, user_id=user_id)
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
                        return Response(response_data,
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            return Response({'message': 'Error occurred while making the request'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VleValidateOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # serializer = VleOtpSerializer(data=request.data)
        # if serializer.is_valid():
        mobile_no = request.data.get('mobile_no')
        otp_code = request.data.get('otp_code')
        vle_id = request.data.get('vle_id')

        if VleOtp.objects.filter(mobile_no=mobile_no).exists():

            if VleOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code).exists():
                response_data = {
                    'status': '00',
                    'message': "OTP verified successfully",
                    'vle_id': vle_id
                }
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
                    return Response({'status': '01', 'message': f'No Employee has been created '
                                                                f'for the provided user_id.',
                                     'week_flag': -1, 'month_flag': -1}, status=status.HTTP_200_OK)
            response = {
                'status': '00',
                'message': 'success',
                'week_flag': 1,
                'month_flag': 1,
                'month_data': [{"loginTarget": "", "visitTarget": "", "disbursementTarget": "",
                                "loginAchieved": "", "visitAchieved": "", "disbursementAchieved": "",
                                "MonthName": "", "MonthId": ""}],
                'current_week_data': [{"loginAchieved": "", "visitAchieved": "", "disbursementAchieved": "",
                                       "weekName": "", "weekId": ""}]
            }
            today_date = date.today()
            month_id = today_date.month
            month = today_date.strftime("%B")
            year = today_date.year
            month_target = EmployeeSetTargetDetails.objects.filter(employee_id=employee_id, month_name=month, year=year)
            if not month_target.exists():
                return Response({'status': '01', 'message': f'Target is not set for you. '
                                                            f'Kindly reach-out to your reporting manager.',
                                 'week_flag': -1, 'month_flag': -1}, status=status.HTTP_200_OK)
            elif month_target.exists():
                month_target = month_target.first()
                response['month_data'][0]['loginTarget'] = str(month_target.login_target)
                response['month_data'][0]['visitTarget'] = str(month_target.visit_target)
                response['month_data'][0]['disbursementTarget'] = str(month_target.disbursement_target)
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
                        filtered_data = EmployeeTargetDetails.objects.filter(employee_id=employee_id,
                                                                             date__range=(start_date, end_date))
                        if not filtered_data.exists():
                            response['week_flag'] = -1
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