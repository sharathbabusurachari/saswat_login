# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
import uuid
from random import randint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import F, Q


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
        return f"{self.first_name} {self.mid_name} {self.last_name}_{self.user_id}"


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

class VleMobileVOtp(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    otp_genration_time = models.DateTimeField(auto_now_add=True)
    otp_expiration_time = models.DateTimeField()
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'vle_mobile_no_verification'

    def __str__(self):
        return self.mobile_no

    def save(self, *args, **kwargs):
        if not self.pk:
            self.otp_expiration_time = datetime.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.otp_genration_time < timezone.now() - timezone.timedelta(minutes=1)


class VleOtp(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    otp_genration_time = models.DateTimeField(auto_now_add=True)
    otp_expiration_time = models.DateTimeField()
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'vle_otp'

    def __str__(self):
        return self.mobile_no

    def save(self, *args, **kwargs):
        if not self.pk:
            self.otp_expiration_time = datetime.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.otp_genration_time < timezone.now() - timezone.timedelta(minutes=1)

# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*------Dashboard API------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_id = models.IntegerField(unique=True)
    country_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = 'country'


class District(models.Model):
    id = models.AutoField(primary_key=True)
    district_id = models.IntegerField(unique=True)
    district_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return self.district_name

    class Meta:
        db_table = 'district'


class DesignationDetails(models.Model):
    id = models.AutoField(primary_key=True)
    designation_id = models.IntegerField(unique=True)
    designation_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return self.designation_name

    class Meta:
        db_table = 'designation_details'


class WeekDetails(models.Model):

    WEEK_DATES_FORMAT = "%d-%d"

    id = models.AutoField(primary_key=True)
    week_number = models.IntegerField(verbose_name="Week Number (e.g. 18)")
    week_name = models.CharField(max_length=20, verbose_name="Week Name (e.g. week18)")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    week_dates = models.CharField(max_length=20, verbose_name="Week Dates", editable=False)
    working_days = models.IntegerField()
    month = models.IntegerField(verbose_name="Month", editable=False)
    month_name = models.CharField(max_length=20, verbose_name="Month Name", editable=False)
    year = models.CharField(max_length=4, verbose_name="Year", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return f"{self.week_name}_{self.month_name}_{self.year}"

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date.month != self.end_date.month or self.start_date.year != self.end_date.year:
                raise ValidationError("Start date and end date must be in the same month and year.")
            if self.start_date > self.end_date:
                raise ValidationError("End date must be greater than or equal to start date")
            overlapping_ranges = WeekDetails.objects.filter(
                start_date__lte=self.end_date,
                end_date__gte=self.start_date
            ).exclude(pk=self.pk)
            if overlapping_ranges.exists():
                raise ValidationError("The date range overlaps with an existing date range.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving
        self.month = self.start_date.month
        self.month_name = self.start_date.strftime('%B')  # Format the start date to get the month name
        self.year = str(self.start_date.year)
        self.week_dates = self.WEEK_DATES_FORMAT % (self.start_date.day, self.end_date.day)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'week_details'


class EmployeeDetails(models.Model):

    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(UserDetails, on_delete=models.CASCADE,
                                 related_name='employees', verbose_name="Employee")
    designation = models.ForeignKey(DesignationDetails, on_delete=models.SET_NULL, verbose_name="Designation",
                                    blank=True, null=True)
    full_name = models.CharField(max_length=255, verbose_name="Employee Full Name")
    mobile_number = models.CharField(max_length=15, verbose_name="Mobile Number", unique=True)
    alternate_mobile_number = models.CharField(max_length=15, verbose_name="Alternate Mobile Number",
                                               blank=True, null=True)
    official_email = models.EmailField(max_length=255, verbose_name="Official Email ID", unique=True,
                                       blank=True, null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                          related_name='reportees', verbose_name="Reporting Manager")
    cluster_head = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='cluster_members', verbose_name="Cluster Head")
    hobli_block = models.CharField(max_length=100, verbose_name="Hobli / Block")
    taluk = models.CharField(max_length=100, verbose_name="Taluk")
    cluster = models.CharField(max_length=100, verbose_name="Cluster")
    district = models.CharField(max_length=100, verbose_name="District")
    state = models.CharField(max_length=100, verbose_name="State")
    full_address = models.TextField(verbose_name="Full address")
    pin_code = models.CharField(max_length=10, verbose_name="PIN CODE")
    work_department = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "employee_details"
        unique_together = ('employee',)


class EmployeeTargetDetails(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE,
                                 related_name='employee_targets', verbose_name="Employee")
    year = models.CharField(max_length=4, verbose_name="Year", editable=False)
    month = models.IntegerField(verbose_name="Month", editable=False)
    month_name = models.CharField(max_length=20, verbose_name="Month Name", editable=False)
    week = models.ForeignKey(WeekDetails, on_delete=models.CASCADE, verbose_name="Week")
    date = models.DateField()
    visit_achieved = models.IntegerField()
    login_achieved = models.IntegerField()
    disbursement_achieved = models.IntegerField()
    version = models.IntegerField(default=1, editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)
    modified_by = models.CharField(max_length=255)

    def __str__(self):
        return self.employee.full_name

    def clean(self):
        super().clean()
        if self.date and self.date > timezone.now().date():
            raise ValidationError("You can not know the Targets achieved by a user for a "
                                  "future date (Correct the Date).")
        if self.week_id and self.date:
            week = WeekDetails.objects.get(pk=self.week_id)
            if not (week.start_date <= self.date <= week.end_date):
                raise ValidationError(f"Date {self.date} is outside the range of selected week: {week.week_name} ({week.start_date} - {week.end_date})")
        if self.employee_id and self.week_id and self.date:
            month = self.date.month
            year = str(self.date.year)
            is_target_set = EmployeeSetTargetDetails.objects.filter(employee_id=self.employee_id, month=month,
                                                                    year=year, week_id=self.week_id)
            if not is_target_set.exists():
                raise ValidationError(f'Kindly set a target first for the employee - {self.employee}, '
                                      f'for the selected week.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving

        if not self.pk:  # Check if it's a new entry
            # Annotate the queryset to count existing entries for the same user and date
            existing_entries_count = EmployeeTargetDetails.objects.filter(
                employee=self.employee,
                date=self.date
            ).annotate(
                num_entries=F('id')
            ).count()
            # Set the version to the count + 1
            self.version = existing_entries_count + 1

        self.month = self.date.month
        self.month_name = self.date.strftime('%B')  # Format the start date to get the month name
        self.year = str(self.date.year)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "employee_target_details"


class EmployeeSetTargetDetails(models.Model):

    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December')
    ]

    YEAR_CHOICES = [(str(i), str(i)) for i in range(2020, 2051)]

    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE,
                                 related_name='employee_set_targets', verbose_name="Employee")
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.CharField(choices=YEAR_CHOICES, max_length=4)
    month_name = models.CharField(max_length=20, verbose_name="Month Name", editable=False)
    week = models.ForeignKey(WeekDetails, on_delete=models.CASCADE, related_name='employee_week_set_targets',
                             verbose_name="Week")
    visit_target = models.IntegerField()
    login_target = models.IntegerField()
    disbursement_target = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)
    modified_by = models.CharField(max_length=255)

    def __str__(self):
        return self.employee.full_name

    def clean(self):
        super().clean()
        if self.employee_id and self.month and self.year and self.week_id:
            if (EmployeeSetTargetDetails.objects.
                    filter(employee=self.employee, month=self.month, year=self.year, week=self.week).exists()):
                month_name = dict(self.MONTH_CHOICES)[self.month]
                raise ValidationError(f"The Target for '{self.week}' has already been set for '{self.employee}' \
                for {month_name}-{self.year}. Kindly delete that entry first and then Create another entry")
        if self.employee_id and self.month and self.year and self.week_id:
            week_identifier_qs = WeekDetails.objects.filter(month=self.month, year=self.year)
            week_identifier_list = list(week_identifier_qs.values_list('id', flat=True))
            if self.week_id not in week_identifier_list:
                month_name = dict(self.MONTH_CHOICES)[self.month]
                raise ValidationError(f"The selected Week - '{self.week}' does not belong to {month_name},{self.year}.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving
        self.month_name = dict(self.MONTH_CHOICES)[self.month]
        super().save(*args, **kwargs)

    class Meta:
        db_table = "employee_set_target_details"


class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'), ('CCPU HOLD', 'CCPU HOLD'), ('SALES HOLD', 'SALES HOLD'),
        ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED'),
        ('E-SIGN RECEIVED', 'E-SIGN RECEIVED'), ('E-SIGN DONE', 'E-SIGN DONE'),
        ('DMS', 'DMS'), ('DISBURSED', 'DISBURSED'), ('AUTHORISED', 'AUTHORISED')
    ]

    id = models.AutoField(primary_key=True)
    saswat_application_number = models.CharField(max_length=10, unique=True)
    loan_id = models.CharField(max_length=10, null=True, blank=True)
    date_of_login = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    customer_name = models.CharField(max_length=255)
    sales_officer = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE, verbose_name="SO (Sales Officer)")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    @property
    def sales_officer_rm(self):
        return self.sales_officer.reporting_manager.full_name if self.sales_officer.reporting_manager.full_name else None

    @property
    def sales_officer_district(self):
        return self.sales_officer.district

    @property
    def sales_officer_cluster(self):
        return self.sales_officer.cluster

    def __str__(self):
        return self.saswat_application_number

    class Meta:
        db_table = 'loan_application'


class Query(models.Model):
    QUERY_STATUS_CHOICES = [
        ('OPEN', 'OPEN'), ('ANSWERED', 'ANSWERED'), ('REOPENED', 'REOPENED'), ('VERIFIED', 'VERIFIED')
    ]

    id = models.AutoField(primary_key=True)
    saswat_application_number = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    query_date = models.DateField()
    question_or_query = models.CharField(max_length=255, verbose_name="Question / Query")
    query_status = models.CharField(choices=QUERY_STATUS_CHOICES, max_length=20)
    remarks_by_so = models.CharField(max_length=255, null=True, blank=True)
    attachment_one = models.FileField(upload_to='query_attachments/', null=True, blank=True, verbose_name="Attachment 1")
    attachment_two = models.FileField(upload_to='query_attachments/', null=True, blank=True, verbose_name="Attachment 2")
    attachment_three = models.FileField(upload_to='query_attachments/', null=True, blank=True, verbose_name="Attachment 3")
    self_remarks_by_admin = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    @property
    def loan_id(self):
        return self.saswat_application_number.loan_id if self.saswat_application_number.loan_id else None

    def __str__(self):
        return str(self.saswat_application_number)

    class Meta:
        db_table = 'query'

class QueryModel(models.Model):
    QUERY_STATUS_CHOICES = [
        ('OPEN', 'OPEN'), ('ANSWERED', 'ANSWERED'), ('REOPENED', 'REOPENED'), ('VERIFIED', 'VERIFIED')
    ]
    id = models.AutoField(primary_key=True)
    saswat_application_number = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    query_id = models.CharField(max_length=6, verbose_name="Query ID")
    query_date = models.DateField()
    question_or_query = models.CharField(max_length=255, verbose_name="Question / Query")
    query_status = models.CharField(choices=QUERY_STATUS_CHOICES, max_length=20)
    remarks_by_ta = models.CharField(max_length=255, null=True, blank=True)
    remarks_by_so = models.CharField(max_length=255, null=True, blank=True)
    version = models.IntegerField(default=1, editable=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    @property
    def loan_id(self):
        return self.saswat_application_number.loan_id if self.saswat_application_number.loan_id else None

    def __str__(self):
        return str(self.saswat_application_number)

    class Meta:
        db_table = 'query_model'


class SoAndTaAttachment(models.Model):
    query = models.ForeignKey(QueryModel, on_delete=models.CASCADE, related_name='attachments')
    so_attachment = models.FileField(upload_to='so_attachments/', null=True, blank=True)
    ta_attachment = models.FileField(upload_to='ta_attachments/', null=True, blank=True)

    class Meta:
        db_table = 'so_and_ta_attachment'
