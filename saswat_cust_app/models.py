# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
import uuid


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number


class UserDetails(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    mid_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    work_dept = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=15)
    designation = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    designation_id = models.CharField(max_length=10,blank=True, null=True)

#     class Meta:
#         unique_together = ('user_id', 'mobile_no')

    def __str__(self):
        return self.first_name


class UserOtp(models.Model):
    # mobile_no = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    otp_genration_time = models.DateTimeField(auto_now_add=True)
    otp_expiration_time = models.DateTimeField()

    def __str__(self):
        return self.mobile_no

    def save(self, *args, **kwargs):

        if not self.pk:
            self.otp_expiration_time = datetime.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.otp_genration_time < timezone.now() - timezone.timedelta(minutes=2)

    # @staticmethod
    # def delete_expired():
    #     expired_otps = UserOtp.objects.filter(otp_expiration_time__lte=datetime.now())
    #     expired_otps.delete()


class GpsModel(models.Model):
    user_id = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    gps_date = models.DateField()
    gps_time = models.TimeField()
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    gender_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.gender


class State(models.Model):
    state_id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=20)

    def __str__(self):
        return self.state


class CustomerTest(models.Model):
    c_id = models.IntegerField(primary_key=True)
    c_name = models.CharField(max_length=20)
    c_dob = models.DateField()
    gender_id = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='customers_gender')
    c_locality = models.CharField(max_length=200)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE, related_name='customers_state')
    c_mobile_no = models.CharField(max_length=10)
    version = models.CharField(max_length=20)
    file = models.FileField(upload_to='documents/', blank=True)
    document_name = models.CharField(max_length=20)
    document_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.c_name

class VleVillageInfo(models.Model):
    vle_id = models.IntegerField(primary_key=True)
    village_name = models.CharField(max_length=30, verbose_name="Village Name")
    post_office = models.CharField(max_length=30, verbose_name="Post Office")
    panchayat = models.CharField(max_length=30, verbose_name="Panchayath")
    hobli_block_kendra = models.CharField(max_length=30, verbose_name="Hobli / Block / Kendra")
    taluk = models.CharField(max_length=30, verbose_name="Taluk")
    district = models.CharField(max_length=30, verbose_name="District")
    pincode = models.CharField(max_length=20, verbose_name="Pincode")
    state = models.CharField(max_length=10, verbose_name="State")
    user_id = models.CharField(max_length=10, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.vle_id)


    class Meta:
        db_table = 'vle_village_info'


class BmcBasicInformation(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="BMC Name")
    address = models.CharField(max_length=100, verbose_name="BMC / Milk Collection Centre Name and Address with PIN code")
    entity_type = models.CharField(max_length=100, verbose_name="BMC / Milk Centre Entity Type")
    dairy_associated = models.CharField(max_length=100, verbose_name="Dairy Associated")
    total_members = models.CharField(max_length=100, verbose_name="Total Members at the milk centre")
    active_milk_pouring_members = models.CharField(max_length=100, verbose_name="Active milk pouring members")
    morning_milk_pouring = models.CharField(max_length=100, verbose_name="Morning Milk pouring at centre")
    evening_milk_pouring = models.CharField(max_length=100, verbose_name="Evening milk pouring at the centre")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.vle_id)
    class Meta:
        db_table = "bmc_basic_info"


class VleBasicInformation(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    vle_name = models.CharField(max_length=100, verbose_name="VLE Name")
    # full_name = models.CharField(max_length=255, verbose_name="VLE Name - Full Name")
    # calling_name = models.CharField(max_length=100, verbose_name="Calling Name")
    vle_age = models.CharField(max_length=100, verbose_name="VLE Age")
    vle_qualifications = models.CharField(max_length=100, verbose_name="VLE Qualifications")
    vle_current_position = models.CharField(max_length=100, verbose_name="VLE Current position at Milk Centre")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.vle_name

    class Meta:
        db_table = "vle_basic_info"


class VleMobileNumber(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    vle_mobile_number = models.CharField(max_length=15, verbose_name="Mobile number of VLE", unique=True)
    otp = models.CharField(max_length=15, verbose_name="OTP")
    alternative_mobile_number = models.CharField(max_length=15, verbose_name="Alternative Mobile number of VLE")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.vle_mobile_number

    class Meta:
        db_table = "vle_mobile_number"


class PhotoOfBmc(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    vle_full_photo = models.ImageField(upload_to='vle_photos/', verbose_name="Full Photo of VLE")
    vle_with_sales_officer_photo = models.ImageField(upload_to='vle_photos/', verbose_name="Photo of VLE with Sales officer and milk centre in background")
    vle_passport_photo = models.ImageField(upload_to='vle_photos/', verbose_name="Passport Photo of VLE")
    bmc_photo_1 = models.ImageField(upload_to='bmc_photos/', verbose_name="Photo of BMC / Milk collection centre 1")
    bmc_photo_2 = models.ImageField(upload_to='bmc_photos/', verbose_name="Photo of BMC / Milk collection centre 2")
    bmc_photo_3 = models.ImageField(upload_to='bmc_photos/', verbose_name="Photo of BMC / Milk collection centre 3")
    bmc_photo_4 = models.ImageField(upload_to='bmc_photos/', verbose_name="Photo of BMC / Milk collection centre 4")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Photo Information"

    class Meta:
        db_table = "photo_of_bmc"



class VLEBankDetails(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    cheque_or_statement = models.ImageField(upload_to='vle_documents/', verbose_name="Cheque or first page of statement or passbook")
    pan_card = models.ImageField(upload_to='vle_documents/', verbose_name="PAN Card")
    id_card = models.ImageField(upload_to='vle_documents/', verbose_name="ID card (Masked AADHAR / Driving license / Passport / Voter ID / Any govt ID)")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return "Bank Account Details of VLE"

    class Meta:
        db_table = "vle_bank_details"


class SkillsAndKnowledge(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    smartphone_literacy = models.CharField(max_length=255, verbose_name="Smartphone literacy")
    financial_literacy = models.CharField(max_length=255, verbose_name="Financial Literacy")
    stability_of_stay = models.CharField(max_length=255, verbose_name="Stability of stay")
    financial_standing = models.CharField(max_length=255, verbose_name="Financial Standing")
    vintage_experience = models.CharField(max_length=255, verbose_name="Vintage / Experience")
    integrity = models.CharField(max_length=255, verbose_name="Integrity")
    financial_standing_sales_officer = models.CharField(max_length=255, verbose_name="Financial Standing from Sales officer understanding")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Skills and Knowledge of VLE"

    class Meta:
        db_table = "skills_and_knowledge"


class VLEEconomicAndSocialStatusInfo(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    financial_standing_actual = models.CharField(max_length=255, verbose_name="Financial Standing - Actual")
    approximate_hh_income = models.CharField(max_length=255, verbose_name="Approximate HH income from all sources")
    network_farmers = models.CharField(max_length=255, verbose_name="Network Farmers")
    loans_taken = models.CharField(max_length=255, verbose_name="Loans taken")
    other_income_source = models.CharField(max_length=255, verbose_name="Other Income source of VLE")
    land_holding = models.CharField(max_length=255, verbose_name="Land holding of VLE")
    social_standing = models.CharField(max_length=255, verbose_name="Social standing (ability to represent Saswat)")
    influence = models.CharField(max_length=255, verbose_name="Influence (ability to handle trouble or day to day issues)")
    reference_name = models.CharField(max_length=255, verbose_name="Reference Check")
    reference_number = models.CharField(max_length=255, verbose_name="Reference Check")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Economic and Social Status Information of VLE"

    class Meta:
        db_table = "economic_and_social_status_info"



class VleNearbyMilkCenterContact(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    # vle = models.ForeignKey('VLE', on_delete=models.CASCADE, related_name='nearby_milk_center_contacts', verbose_name="VLE")
    name = models.CharField(max_length=255, verbose_name="Name of the person", blank=True, null=True)
    mobile_number = models.CharField(max_length=15, verbose_name="Mobile number", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name="Address of milk collection centre", blank=True, null=True)
    reason_not_provided = models.CharField(max_length=255, blank=True, null=True, verbose_name="Reason for not providing contacts (Leave this blank if above 3 fields are filled")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "vle_nearby_milk_center_contact"


class VillageDetails(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    water_sources = models.CharField(max_length=255, verbose_name="Water sources details")
    number_of_houses = models.CharField(max_length=255, verbose_name="Number of houses in village")
    voting_number = models.CharField(max_length=255, verbose_name="Voting number at the village")
    approximate_population = models.CharField(max_length=255, verbose_name="Approximate village population")
    description = models.CharField(max_length=255, verbose_name="Description")
    name_of_financial_institution = models.CharField(max_length=255, verbose_name="Name of other financial institution providing loans")
    financial_institution_description = models.CharField(max_length=255, verbose_name="Financial Institution Description")
    dairy_name = models.CharField(max_length=255, verbose_name="Name of other milk center Dairy name")
    total_members = models.CharField(max_length=255, verbose_name="Total Members at the milk centre (Active milk pouring and non-milk pouring) ")
    active_milk_pouring_members = models.CharField(max_length=255, verbose_name="Active milk pouring members ")
    morning_milk_pouring = models.CharField(max_length=255, verbose_name="Morning Milk pouring at centre ")
    evening_milk_pouring = models.CharField(max_length=255, verbose_name="Evening Milk pouring at the centre ")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Village Social, Nature, and Economic Details"

    class Meta:
        db_table = "village_details"