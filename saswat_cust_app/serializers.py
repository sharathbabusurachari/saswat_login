# serializers.py
from rest_framework import serializers
from .models import (UserOtp, GpsModel, CustomerTest, Gender, State,
                     VleVillageInfo, BmcBasicInformation, VleBasicInformation, VleMobileNumber,
                     PhotoOfBmc, VLEBankDetails, SkillsAndKnowledge, VLEEconomicAndSocialStatusInfo,
                     VleNearbyMilkCenterContact, VillageDetails, VleMobileVOtp, VleOtp,
                     LoanApplication, QueryModel, SignInSignOut, QnaAttachment, ShortenedQueries, UserDetails,
                     EmployeeDetails,
                     ESign, EMICollections,
                     Collection, ModesOfPayment, CollectionPayment, CollectionType, AutopayAssigned, LoanAutoPayBase,
                     CollectionAutopay)

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
    user_id = serializers.PrimaryKeyRelatedField(queryset=UserDetails.objects.all(), required=False, write_only=True)
    class Meta:
        model = VleNearbyMilkCenterContact
        fields = ['vle_id', 'name', 'mobile_number', 'address', 'reason_not_provided',
                  'user_id', 'remarks', 'uuid_id', 'created_at', 'updated_at', 'new_remark']

    def update(self, instance, validated_data):
        new_remark = validated_data.pop('new_remark', None)
        user_id = validated_data.pop('user_id', None)
        if user_id:
            instance.user_id = user_id
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
    document_name = serializers.SerializerMethodField()


    class Meta:
        model = QueryModel
        fields = '__all__'

    def get_loan_id(self, obj):
        return obj.loan_id

    def get_document_name(self, obj):
        return obj.document.document_name if obj.document else None

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


    class Meta:
        model = QueryModel
        fields = '__all__'

    def create(self, validated_data):
        version = self.context.get('version', None)
        saswat_application_number = validated_data.pop('saswat_application_number', None)
        shortened_query_str = validated_data.pop('shortened_query', None)
        query_id = validated_data.get('query_id')

        if saswat_application_number:
            saswat_application = LoanApplication.objects.get(saswat_application_number=saswat_application_number)
            validated_data['saswat_application_number'] = saswat_application

        if shortened_query_str:
            shortened_query_instance = ShortenedQueries.objects.get(shortened_query=shortened_query_str)
            validated_data['shortened_query'] = shortened_query_instance


        if version is not None:
            max_version = QueryModel.objects.filter(query_id=query_id).aggregate(Max('version'))['version__max']
            validated_data['version'] = (max_version or 0) + 1

        query = QueryModel.objects.create(**validated_data)
        return query

    def get_loan_id(self, obj):
        return obj.loan_id

class SignInSignOutSerializer(serializers.ModelSerializer):
    gps_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = SignInSignOut
        fields = '__all__'


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    designation_name = serializers.SerializerMethodField()

    class Meta:

        model = EmployeeDetails

        fields = ['id', 'full_name', 'designation', 'designation_name', 'mobile_number', 'official_email']

    def get_designation_name(self, obj):
        return obj.designation.designation_name

class ESignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESign
        fields = '__all__'


class QueryStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryModel
        fields = ['query_status']


class EMICollectionsSerializer(serializers.ModelSerializer):
    paid_status = serializers.SerializerMethodField()
    class Meta:
        model = EMICollections
        fields = ['id', 'lender_loan_id', 'customer_name', 'disbursed_amount', 'installment_no',
                  'emi_amt', 'due_date', 'applicant_mobile_no', 'co_applicant_mobile_no', 'village_details',
                  'block', 'taluk', 'cluster', 'payment_row_id', 'paid_status']

    def get_paid_status(self, obj):
        return obj.paid_status if obj.paid_status is not None else ""


class CollectionSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    prospect_code = serializers.SerializerMethodField()


    class Meta:
        model = Collection
        fields = '__all__'

    def get_customer_name(self, obj):
        return obj.loan_details.customer_name if obj.loan_details else None

    def get_prospect_code(self, obj):
        return obj.loan_details.lender_loan_id if obj.loan_details else None


class ModesOfPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModesOfPayment
        fields = '__all__'


class CollectionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionType
        fields = '__all__'


class CollectionPaymentSerializer(serializers.ModelSerializer):
    loan_id = serializers.CharField(write_only=True)

    class Meta:
        model = CollectionPayment
        fields = '__all__'

    def create(self, validated_data):
        loan_id = validated_data.pop('loan_id')
        collection = Collection.objects.filter(loan_details__lender_loan_id=loan_id).first()
        validated_data['loan_id'] = collection
        collection_payment = CollectionPayment.objects.create(**validated_data)
        return collection_payment

    def update(self, instance, validated_data):
        loan_id = validated_data.pop('loan_id', None)

        if loan_id:
            collection = Collection.objects.filter(loan_details__lender_loan_id=loan_id).first()
            if collection:
                instance.loan_id = collection

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class LoanAutoPayBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanAutoPayBase
        fields = '__all__'


class AutopayAssignedSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    loan_id = serializers.SerializerMethodField()

    class Meta:
        model = AutopayAssigned
        # fields = '__all__'
        fields = ['id', 'customer_name', 'loan_id',
                  'status', 'start_date', 'end_date', "employee_details", "loan_details",
                  ]
    def get_customer_name(self, obj):
        return obj.loan_details.customer_name if obj.loan_details else None

    def get_loan_id(self, obj):
        return obj.loan_details.lender_loan_id if obj.loan_details else None


# class LoanAutoPayRequestStatusSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = LoanAutoPayRequestStatus
#         fields = '__all__'
#
#
# class LoanAutoPaySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = LoanAutoPay
#         fields = '__all__'


class CollectionAutopaySerializer(serializers.ModelSerializer):
    loan_id = serializers.CharField(write_only=True)
    max_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        # default=100000.00,
        required=False
    )
    print(loan_id)

    class Meta:
        model = CollectionAutopay
        fields = '__all__'

    def create(self, validated_data):
        loan_id = validated_data.pop('loan_id')
        print(loan_id)
        collection = AutopayAssigned.objects.filter(loan_details__lender_loan_id=loan_id).first()
        validated_data['max_amount'] = "100000.00"
        validated_data['loan_id'] = collection
        collection_payment = CollectionAutopay.objects.create(**validated_data)
        return collection_payment

    def update(self, instance, validated_data):
        loan_id = validated_data.pop('loan_id', None)

        if loan_id:
            collection = AutopayAssigned.objects.filter(loan_details__lender_loan_id=loan_id).first()
            if collection:
                instance.loan_id = collection

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance



