# serializers.py
from rest_framework import serializers
from .models import (UserOtp, GpsModel, CustomerTest, Gender, State,
                     VleVillageInfo, BmcBasicInformation, VleBasicInformation, VleMobileNumber,
                     PhotoOfBmc, VLEBankDetails, SkillsAndKnowledge, VLEEconomicAndSocialStatusInfo,
                     VleNearbyMilkCenterContact, VillageDetails, VleMobileVOtp, VleOtp,
                     LoanApplication, QueryModel, SignInSignOut, QnaAttachment, ShortenedQueries)

from rest_framework.response import Response
from rest_framework import status
import random
from django.db.models import Max

# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = ('phone_number', 'otp_code')
#


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOtp
        fields = ('mobile_no', 'otp_code', 'otp_generation_time')


class GpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpsModel
        fields = '__all__'

class CustomerTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerTest
        fields = '__all__'

    def create(self, validated_data):
        if isinstance(validated_data, list):
            return [self.create_single_object(item) for item in validated_data]
        else:
            return self.create_single_object(validated_data)

    def create_single_object(self, validated_data):

        return CustomerTest.objects.create(**validated_data)

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ('gender_id', 'gender')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('state_id', 'state')

class VleVillageInfoSerializer(serializers.ModelSerializer):
    vle_id = serializers.IntegerField(required=False)
    class Meta:
        model = VleVillageInfo
        fields = '__all__'

    def create(self, validated_data):
        try:
            vle_id = validated_data.get('vle_id', None)
            if vle_id == 0:
                random_id = random.randint(1000000, 9999999)
                while VleVillageInfo.objects.filter(vle_id=random_id).exists():
                    random_id = random.randint(1000000, 9999999)
                validated_data['vle_id'] = random_id
                return VleVillageInfo.objects.create(**validated_data)
            else:
                vle_id_update = VleVillageInfo.objects.get(vle_id=vle_id)
                for key, value in validated_data.items():
                    setattr(vle_id_update, key, value)
                vle_id_update.save()
                return vle_id_update
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BmcBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BmcBasicInformation
        fields = '__all__'


class VleBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VleBasicInformation
        fields = '__all__'


class VleMobileNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VleMobileNumber
        fields = '__all__'


class PhotoOfBmcSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoOfBmc
        fields = '__all__'


class VLEBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VLEBankDetails
        fields = '__all__'


class SkillsAndKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillsAndKnowledge
        fields = '__all__'


class VLEEconomicAndSocialStatusInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VLEEconomicAndSocialStatusInfo
        fields = '__all__'


class VleNearbyMilkCenterContactSerializer(serializers.ModelSerializer):
    new_remark = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = VleNearbyMilkCenterContact
        fields = ['vle_id', 'name', 'mobile_number', 'address', 'reason_not_provided',
                  'user_id', 'remarks', 'uuid_id', 'created_at', 'updated_at', 'new_remark']

    def update(self, instance, validated_data):
        new_remark = validated_data.pop('new_remark', None)
        if new_remark:
            if not isinstance(instance.remarks, list):
                instance.remarks = []
            instance.remarks.append(new_remark)
        return super().update(instance, validated_data)



class VillageDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillageDetails
        fields = '__all__'
class VleMobileVOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = VleMobileVOtp
        fields = ('vle_id', 'mobile_no', 'otp_code', 'otp_generation_time')


class VleOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = VleOtp
        fields = ('vle_id', 'mobile_no', 'otp_code', 'otp_generation_time')

# -----------------------------------*------------Query API-------------*--------------------------------------*--------


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'


class QnaAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAttachment
        fields = '__all__'


class ShortenedQueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedQueries
        fields = ['shortened_query', 'description', 'additional_info']


class GetQuerySerializer(serializers.ModelSerializer):
    saswat_application_number = serializers.CharField(read_only=True)
    shortened_queries = serializers.SerializerMethodField()
    loan_id = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    additional_info = serializers.SerializerMethodField()

    class Meta:
        model = QueryModel
        fields = '__all__'

    def get_loan_id(self, obj):
        return obj.loan_id

    def get_shortened_queries(self, obj):
        return obj.shortened_query.shortened_query if obj.shortened_query else None

    def get_description(self, obj):
        return obj.shortened_query.description if obj.shortened_query else None

    def get_additional_info(self, obj):
        return obj.shortened_query.additional_info if obj.shortened_query else None


class NewQuerySerializer(serializers.ModelSerializer):
    saswat_application_number = serializers.CharField(write_only=True)
    loan_id = serializers.SerializerMethodField()
    shortened_query = serializers.CharField(write_only=True)
    description = serializers.CharField(write_only=True)
    additional_info = serializers.CharField(write_only=True)

    class Meta:
        model = QueryModel
        fields = '__all__'

    def create(self, validated_data):
        version = self.context.get('version', None)
        saswat_application_number = validated_data.pop('saswat_application_number', None)
        shortened_query_str = validated_data.pop('shortened_query', None)
        description_str = validated_data.pop('description', None)
        additional_info_str = validated_data.pop('additional_info', None)
        query_id = validated_data.get('query_id')

        if saswat_application_number:
            saswat_application = LoanApplication.objects.get(saswat_application_number=saswat_application_number)
            validated_data['saswat_application_number'] = saswat_application

        if shortened_query_str:
            shortened_query_instance = ShortenedQueries.objects.get(shortened_query=shortened_query_str)
            validated_data['shortened_query'] = shortened_query_instance

        if description_str:
            description_str_instance = ShortenedQueries.objects.get(shortened_query=description_str)
            validated_data['description'] = description_str_instance

        if additional_info_str:
            additional_info_instance = ShortenedQueries.objects.get(shortened_query=additional_info_str)
            validated_data['additional_info'] = additional_info_instance

        if version is not None:
            max_version = QueryModel.objects.filter(query_id=query_id).aggregate(Max('version'))['version__max']
            validated_data['version'] = (max_version or 0) + 1

        query = QueryModel.objects.create(**validated_data)
        return query

    def get_loan_id(self, obj):
        return obj.loan_id

class SignInSignOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignInSignOut
        fields = '__all__'