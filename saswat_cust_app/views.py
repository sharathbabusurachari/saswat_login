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
from saswat_cust_app.serializers import OTPSerializer, GpsSerializer, CustomerTestSerializer, GenderSerializer, StateSerializer
from datetime import datetime, timedelta
import requests
# from rest_framework.authentication import SessionAuthentication
from .authenticate import MobileNumberAuthentication
from django.utils import timezone


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


class CustomerTestView(ListCreateAPIView):
    co_applicant_det = CustomerTest.objects.all()
    serializer_class = CustomerTestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            # Handle any errors that occur during creation
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

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