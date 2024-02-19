import string
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .utils import is_valid_indian_mobile_number
from .models import OTP, UserOtp, UserDetails
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import random
from saswat_cust_app.serializers import OTPSerializer
from datetime import datetime, timedelta
import requests
from rest_framework.authentication import SessionAuthentication
from .authenticate import MobileNumberAuthentication
from django.utils import timezone

class SendOTPAPIView(APIView):

    def post(self, request, *args, **kwargs):
        mobile_no = request.data.get('mobile_no')
        url = 'http://20.235.246.32:8080/message/telspielmessage'
        try:
            if UserOtp.objects.filter(mobile_no=mobile_no).exists():
                return Response({'Error': 'OTP has already sent.'})

            # if not is_valid_indian_mobile_number(mobile_no):
            #     return JsonResponse({'error': 'Invalid Indian mobile number format'}, status=400)
            if UserDetails.objects.filter(mobile_no=mobile_no).exists():
                otp_code = str(random.randint(1000, 9999))
                data = {
                    'otp': otp_code,
                    'dest': mobile_no
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
                    return Response(response_data, status=200)
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






# class ValidateOTPAPIView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         mobile_no = request.data.get('mobile_no')
#         otp_entered = request.data.get('otp_code')
#
#         try:
#             user_details = UserDetails.objects.get(mobile_no=mobile_no)
#             try:
#                 otp_record = UserOtp.objects.get(mobile_no=user_details)
#             except UserOtp.DoesNotExist:
#                 otp_record = UserOtp.objects.create(mobile_no=str(mobile_no))
#             if otp_record.is_expired():
#                 otp_record.delete()
#                 return Response({'message': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
#             elif otp_record.otp_code == otp_entered:
#                 otp_record.delete()
#                 return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
#         except UserDetails.DoesNotExist:
#             return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except UserOtp.DoesNotExist:
#             return Response({'message': 'No OTP found for this user'}, status=status.HTTP_404_NOT_FOUND)

# class ValidateOTPAPIView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         mobile_no = request.data.get('mobile_no')
#         otp_code = request.data.get('otp_code')
#         # if not is_valid_indian_mobile_number(mobile_no):
#         #     return JsonResponse({'error': 'Invalid Indian mobile number format'}, status=400)
#
#         if UserDetails.objects.filter(mobile_no=mobile_no).exists():
#             otp_instance = get_object_or_404(UserOtp, mobile_no=str(mobile_no), otp_code=otp_code)
#             otp_instance.delete()
#
#             return JsonResponse({'success': 'OTP verified successfully'}, status=200)
#         else:
#             return JsonResponse({'error': 'Invalid OTP'}, status=404)
#
class ValidateOTPAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [MobileNumberAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_no = serializer.validated_data['mobile_no']
            otp_code = serializer.validated_data['otp_code']

            if UserDetails.objects.filter(mobile_no=mobile_no).exists():
                check_valid_time = datetime.now() - timedelta(minutes=2)
                user_det = UserDetails.objects.filter(mobile_no=mobile_no).first()
                valid_otp_mobile = UserOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code).first()
                valid_otp_time = UserOtp.objects.filter(mobile_no=mobile_no, otp_expiration_time__lt=timezone.now()).first()

                verify_user_otp = UserOtp.objects.filter(mobile_no=mobile_no, otp_code=otp_code,
                                             otp_genration_time__gte=check_valid_time).first()
                print(valid_otp_mobile, valid_otp_time, verify_user_otp)
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
                    return Response(response_data,status=200)
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


























































