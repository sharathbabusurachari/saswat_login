from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


# class UserModel(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user.username} - {self.id}'

# Create your models here.
class P01BusinessLoanAppForm(models.Model):
    DATA_ENTRY_CHOICES = [
        ('Inprogress', 'Inprogress'),
        ('Completed', 'Completed'),
        ('Review', 'Review'),
        ('Re-Edit', 'Re-Edit'),
        ('Verified', 'Verified'),
    ]

    APP_STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Rejected', 'Rejected'),
        ('Approved', 'Approved'),
        ('Disbursed', 'Disbursed'),
        ('Loan Closed', 'Loan Closed'),
        ('E-Sign Done', 'E-Sign Done'),
        ('E-Sign Received', 'E-Sign Received'),
        ('Pending', 'Pending'),
        ('Credit', 'Credit'),
        ('Sales Hold', 'Sales Hold'),
        ('DMS', 'DMS'),
        ('Approved-Dropped', 'Approved-Dropped'),
    ]
    app_no = models.CharField(verbose_name="Application No", max_length=10, primary_key=True)
    app_date = models.DateField(verbose_name="Application Date")
    data_entry_status = models.CharField(choices=DATA_ENTRY_CHOICES, max_length=20, default='Inprogress')
    app_status = models.CharField(choices=APP_STATUS_CHOICES, max_length=20)
    city = models.CharField(max_length=50, verbose_name="City")
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.app_no



class P02FinancialRequirement(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    purpose_of_loan = models.CharField(max_length=50, verbose_name="Purpose of loan")
    loan_type = models.CharField(max_length=50, verbose_name="Loan Type")
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan amount")
    desire_tenure = models.IntegerField(verbose_name="Desire Tenure")
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.app_no)


class P09CoApplicant(models.Model):
    PAN_AND_FORM_CHOICES = [
        ('PAN', 'Pan'),
        ('FORM60', 'Form 60'),
    ]

    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    father_or_spouse_name = models.CharField(max_length=100, verbose_name="Father/Spouse's Name")
    pan_and_form_sixty = models.CharField(max_length=10, choices=PAN_AND_FORM_CHOICES, default='Pan')
    pan_number = models.CharField(max_length=10, verbose_name="PAN No", blank=True, null=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15, verbose_name="Mobile")
    email = models.EmailField(max_length=100, verbose_name="E-mail", blank=True, null=True)
    address_1 = models.CharField(max_length=200, verbose_name="Address 1")
    state_1 = models.CharField(max_length=100, verbose_name="State")
    city_1 = models.CharField(max_length=100, verbose_name="City")
    pincode_1 = models.CharField(max_length=10, verbose_name="Pincode")
    address_2 = models.CharField(max_length=200, verbose_name="Address 2", blank=True, null=True)
    state_2 = models.CharField(max_length=100, verbose_name="State 2", blank=True, null=True)
    city_2 = models.CharField(max_length=100, verbose_name="City 2", blank=True, null=True)
    pincode_2 = models.CharField(max_length=10, verbose_name="Pincode 2", blank=True, null=True)
    OWNERSHIP_CHOICES = [
        ('Owned', 'Owned'),
        ('Rented', 'Rented'),
    ]
    ownership_status = models.CharField(max_length=100, choices=OWNERSHIP_CHOICES)
    applicant_photo = models.ImageField(upload_to='applicant_photos/', verbose_name="Applicant photo(signed)")
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class P04BankAccountDetail(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=11, verbose_name="IFSC code")
    account_number = models.CharField(max_length=20)
    micr_code = models.CharField(max_length=9, verbose_name="MICR code", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.account_name}'s {self.bank_name} Account"


class P05CustomerConsent(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    applied_amount = models.DecimalField(max_digits=12, decimal_places=2,verbose_name="Applied Amount INR")
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Applied Amount: ₹{self.applied_amount}"


# class KycDeclaration(models.Model):
#     kyc_declaration_of_applicants = models.BooleanField(verbose_name="KYC Declaration of Applicants")
#     kyc_declaration_of_co_applicants = models.BooleanField(verbose_name="KYC Declaration of Co-Applicants")
#
#     def __str__(self):
#         return f"KYC Declaration of - {self.id}"


class P06GstDeclaration(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=100)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"GST Declaration - Applicant: {self.applicant_name}"


class P07ReferenceOne(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    contact_details = models.CharField(max_length=100)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class P08ReferenceTwo(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    contact_details = models.CharField(max_length=100)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class P03Applicant(models.Model):
    PAN_AND_FORM_CHOICES = [
        ('PAN', 'Pan'),
        ('FORM60', 'Form 60'),
    ]
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    father_or_spouse_name = models.CharField(max_length=100, verbose_name="Father/Spouse's Name")
    pan_and_form_sixty = models.CharField(max_length=10, choices=PAN_AND_FORM_CHOICES, default='Pan')
    pan_number = models.CharField(max_length=10, verbose_name="PAN No", blank=True, null=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15, verbose_name="Mobile")
    email = models.EmailField(max_length=100, verbose_name="E-mail", blank=True, null=True)
    address_1 = models.CharField(max_length=200, verbose_name="Address 1")
    state_1 = models.CharField(max_length=100, verbose_name="State")
    city_1 = models.CharField(max_length=100, verbose_name="City")
    pincode_1 = models.CharField(max_length=10, verbose_name="Pincode")
    address_2 = models.CharField(max_length=200, verbose_name="Address 2", blank=True, null=True)
    state_2 = models.CharField(max_length=100, verbose_name="State 2", blank=True, null=True)
    city_2 = models.CharField(max_length=100, verbose_name="City 2", blank=True, null=True)
    pincode_2 = models.CharField(max_length=10, verbose_name="Pincode 2", blank=True, null=True)
    OWNERSHIP_CHOICES = [
        ('Owned', 'Owned'),
        ('Rented', 'Rented'),
    ]
    ownership_status = models.CharField(max_length=100, choices=OWNERSHIP_CHOICES)
    applicant_photo = models.ImageField(upload_to='applicant_photos/', verbose_name="Applicant photo(signed)")
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class P23InsuranceApplicationToSaswat(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    loan_facility = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan facility (Rs)",blank=True, null=True)
    insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Insurance premium (Rs)", blank=True, null=True)
    to_specified_paravet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To specified Paravet (Rs)", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"Details - {self.date}"


class P22InsuranceApplicationToAmbit(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date", blank=True, null=True)
    loan_facility = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan facility (Rs)", blank=True, null=True)
    insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Insurance premium (Rs)", blank=True, null=True)
    to_specified_paravet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To specified Paravet (Rs)", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"Details - {self.date}"


class P10Attachment(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    applicant_adhaar = models.FileField(upload_to='attachments/', verbose_name="Applicant Adhaar(Masked and signed-OSV)")
    # applicant_pan = models.FileField(upload_to='attachments/', verbose_name="Applicant PAN(Signed-OSV)")
    applicant_pan_or_form_sixty = models.FileField(upload_to='attachments/', verbose_name="Applicant PAN/Form 60")
    applicant_voter_id = models.FileField(upload_to='attachments/', verbose_name="Applicant Voter  Id(Optional)", blank=True, null=True)
    co_applicant_adhaar = models.FileField(upload_to='attachments/', verbose_name="Co-Applicant Adhaar(Masked and signed)")
    # co_applicant_pan = models.FileField(upload_to='attachments/', verbose_name="Co-Applicant PAN(Signed)")
    co_applicant_pan_or_form_sixty = models.FileField(upload_to='attachments/', verbose_name="Co Applicant PAN/Form 60")
    bankers_verification = models.FileField(upload_to='attachments/', verbose_name="Bankers Verification", blank=True, null=True)
    indemnity_bond_signature = models.FileField(upload_to='attachments/', verbose_name="Indemnity bond - signature /name/dob(With notorized affidavit)", blank=True, null=True)
    milk_statement = models.FileField(upload_to='attachments/', verbose_name="Milk statement")
    bank_statement = models.FileField(upload_to='attachments/', verbose_name="Bank statement")
    living_certificate = models.FileField(upload_to='attachments/', verbose_name="Living certificate", blank=True, null=True)
    nach_mandate = models.FileField(upload_to='attachments/', verbose_name="NACH Mandate",  blank=True, null=True)
    spdc_pdc_cheques = models.FileField(upload_to='attachments/', verbose_name="SPDC/PDC Cheques(Applicant & co-applicant)",  blank=True, null=True)
    address_proof = models.FileField(upload_to='attachments/', verbose_name="Address proof(ration card, electricity bill, pahani, gas cylender book, etc..)",  blank=True, null=True)
    anexure = models.FileField(upload_to='attachments/', verbose_name="Anexure", blank=True, null=True)
    vernacular_signature = models.FileField(upload_to='attachments/', verbose_name="Vernacular Signature", blank=True,null=True)
    ndc_checklist = models.FileField(upload_to='attachments/', verbose_name="NDC Checklist",  blank=True, null=True)
    login_checklist = models.FileField(upload_to='attachments/', verbose_name="LoginChecklist",  blank=True, null=True)
    loan_agreement = models.FileField(upload_to='attachments/', verbose_name="LOAN Agreement", blank=True, null=True)
    audit_trail = models.FileField(upload_to='attachments/', verbose_name="Audit Trail", blank=True,null=True)
    loan_deduction_table = models.FileField(upload_to='attachments/', verbose_name="Loan deduction Table", blank=True,null=True)
    insurance = models.FileField(upload_to='attachments/', verbose_name="Insurance", blank=True, null=True)
    field_visit_home = models.FileField(upload_to='attachments/', verbose_name="Field visit photo (Home)", blank=True, null=True)
    field_visit_cattle = models.FileField(upload_to='attachments/', verbose_name="Field visit photo (cattle)", blank=True, null=True)
    field_visit_shed = models.FileField(upload_to='attachments/', verbose_name="Field visit photo (shed)", blank=True, null=True)
    cam_sheet = models.FileField(upload_to='attachments/', verbose_name="CAM sheet",  blank=True, null=True)
    post_disbursal_doc = models.FileField(upload_to='attachments/', verbose_name="Post Disbursal Document Attachment", blank=True, null=True)
    additional_1 = models.FileField(upload_to='attachments/', verbose_name="Additional 1 Attachment", blank=True, null=True)
    additional_2 = models.FileField(upload_to='attachments/', verbose_name="Additional 2 Attachment", blank=True, null=True)
    additional_3 = models.FileField(upload_to='attachments/', verbose_name="Additional 3 Attachment", blank=True, null=True)
    additional_4 = models.FileField(upload_to='attachments/', verbose_name="Additional 4 Attachment", blank=True, null=True)
    additional_5 = models.FileField(upload_to='attachments/', verbose_name="Additional 5 Attachment", blank=True, null=True)
    remarks = models.TextField(verbose_name="Additional Remarks", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)


class P12SequrityPostDatedCheques(models.Model):
    app_no = models.ForeignKey(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    cheque_no_from = models.IntegerField(verbose_name="Cheque Number From", blank=True, null=True)
    cheque_no_to = models.IntegerField(verbose_name="Cheque Number To",  blank=True, null=True)
    Amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    issuing_bank_name = models.CharField(max_length=30, verbose_name="Issuing bank name",  blank=True, null=True)
    issuing_bank_ac_no = models.CharField(max_length=30, verbose_name="Issuing bank Acc Number",  blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.issuing_bank_name)


class P11PostDatedCheques(models.Model):
    app_no = models.ForeignKey(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    cheque_no_from = models.IntegerField(verbose_name="Cheque Number From",  blank=True, null=True)
    cheque_no_to = models.IntegerField(verbose_name="Cheque Number To",  blank=True, null=True)
    Amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    issuing_bank_name = models.CharField(max_length=30, verbose_name="Issuing bank name",  blank=True, null=True)
    issuing_bank_ac_no = models.CharField(max_length=30, verbose_name="Issuing bank Acc Number", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.issuing_bank_name)


class P13SpdcAndPdcForm(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    loan_agreement_dated = models.DateField(blank=True, null=True)
    name_of_borrower_or_co_borrower = models.CharField(max_length=30, verbose_name="Name of borrower/co-borrower",  blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name_of_borrower_or_co_borrower)

####################

class P14PdSheetPersonalDetails(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, verbose_name="Name of customer", blank=True, null=True)
    customer_date_of_birth = models.DateField(verbose_name="Date of birth of customer", blank=True, null=True)
    customer_age = models.IntegerField(verbose_name="Age of customer", blank=True, null=True)
    customer_kyc_source = models.CharField(max_length=100, verbose_name="KYC source of customer",  blank=True, null=True)

    co_applicant_name = models.CharField(max_length=100, verbose_name="Name of co-applicant", blank=True, null=True)
    co_applicant_date_of_birth = models.DateField(verbose_name="Date of birth of co-applicant", blank=True, null=True)
    co_applicant_age = models.IntegerField(verbose_name="Age of co-applicant", blank=True, null=True)
    co_applicant_kyc_source = models.CharField(max_length=100, verbose_name="KYC source of co-applicant", blank=True, null=True)

    total_dependents = models.IntegerField(verbose_name="Total Number of dependents", blank=True, null=True)
    adults_count = models.IntegerField(verbose_name="Adults count", blank=True, null=True)
    children_count = models.IntegerField(verbose_name="Children count",  blank=True, null=True)

    residence_address = models.CharField(max_length=255, verbose_name="Residence address",  blank=True, null=True)
    OWNED_RENTED_CHOICES = [
        ('Owned', 'Owned'),
        ('Rented', 'Rented'),
    ]
    residence_owned_rented = models.CharField(max_length=10, choices=OWNED_RENTED_CHOICES, verbose_name="Owned/rented",  blank=True, null=True)
    residence_stability_years = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Residence stability in years", blank=True, null=True)
    kyc_source = models.CharField(max_length=100, verbose_name="KYC source", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer_name}'s Personal Details"


class P15PdBusinessDetails(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    business_address = models.CharField(max_length=255, verbose_name="Business address", blank=True, null=True)
    OWNED_RENTED_CHOICES = [
        ('Owned', 'Owned'),
        ('Rented', 'Rented'),
    ]
    business_owned_rented = models.CharField(max_length=10, choices=OWNED_RENTED_CHOICES, verbose_name="Owned/rented", blank=True, null=True)
    business_stability_at_present_address_years = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Business stability at present address in years")
    total_business_stability_years = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Total business stability in years")
    total_experience_in_business_line_years = models.DecimalField(max_digits=12, decimal_places=2,blank=True, null=True, verbose_name="Total experience in business line in years")
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Business Details at {self.business_address}"


class P16PdLoanDetails(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    nature_of_business = models.CharField(max_length=255, verbose_name="Nature of business", blank=True, null=True)
    loan_type = models.CharField(max_length=100, verbose_name="Loan type",  blank=True, null=True)
    applied_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Applied amount", blank=True, null=True)
    applied_tenure = models.CharField(max_length=255, verbose_name="Applied tenure", blank=True, null=True)
    comfortable_emi = models.CharField(max_length=25, verbose_name="Comfortable EMI as per customer", blank=True, null=True)
    # comfortable_emi = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Comfortable EMI as per customer")
    # BORROWER_TYPE_CHOICES = [
    #     ('Individual', 'Individual'),
    #     ('Company', 'Company'),
    # ]
    borrower_type = models.CharField(max_length=100, verbose_name="Borrower type", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Loan Details for {self.nature_of_business}"


class P17PdTotalAssets(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    home = models.CharField(max_length=255, verbose_name="Home",  blank=True, null=True)
    business = models.CharField(max_length=255, verbose_name="Business",  blank=True, null=True)
    agri_land = models.CharField(max_length=255, verbose_name="Agri land",  blank=True, null=True)
    additional_income = models.CharField(max_length=255, verbose_name="Additional income (others)", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.business)


class P18PdVisit(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    # reference_check_visit = models.BooleanField(verbose_name="Reference check/visit", default=False)
    residential_house_visit = models.BooleanField(verbose_name="Residential house visit", default=False, blank=True, null=True)
    residential_visit_done_by = models.CharField(max_length=100, verbose_name="Done by (Residential house visit)", blank=True, null=True)
    business_premises_visit = models.BooleanField(verbose_name="Business premises visit", default=False,  blank=True, null=True)
    business_visit_done_by = models.CharField(max_length=100, verbose_name="Done by (Business premises visit)",  blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.residential_visit_done_by)


class P19PdBureauSummary(models.Model):
    # MFI Loan details
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    mfi_loan_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type MFI Loan amount", blank=True, null=True)
    mfi_loan_tenure = models.IntegerField(verbose_name="Loan Type MFI Loan tenure", blank=True, null=True)
    mfi_emi_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type MFI EMI amount", blank=True,null=True)
    mfi_emi_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type MFI EMI paid", blank=True, null=True)
    mfi_emi_remaining = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type MFI EMI remaining", blank=True, null=True)

    # KCC Loan details
    kcc_loan_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type KCC Loan amount", blank=True, null=True)
    kcc_loan_tenure = models.IntegerField(verbose_name="Loan Type KCC Loan tenure", blank=True, null=True)
    kcc_emi_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type KCC EMI amount", blank=True, null=True)
    kcc_emi_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type KCC EMI paid", blank=True, null=True)
    kcc_emi_remaining = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type KCC EMI remaining",blank=True, null=True)

    # Personal Loan details
    personal_loan_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Personal Loan amount", blank=True, null=True)
    personal_loan_tenure = models.IntegerField(verbose_name="Loan Type Personal Loan tenure", blank=True, null=True)
    personal_emi_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Personal Loan EMI amount", blank=True, null=True)
    personal_emi_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Personal Loan EMI paid", blank=True, null=True)
    personal_emi_remaining = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Personal Loan EMI remaining", blank=True, null=True)

    # Tractor Loan details
    tractor_loan_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Tractor Loan amount", blank=True, null=True)
    tractor_loan_tenure = models.IntegerField(verbose_name="Loan Type Tractor Loan tenure", blank=True,null=True)
    tractor_emi_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Tractor Loan EMI amount", blank=True, null=True)
    tractor_emi_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Tractor Loan EMI paid", blank=True, null=True)
    tractor_emi_remaining = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Tractor Loan EMI remaining", blank=True,null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.mfi_loan_amt)


class P20PdMiscellaneousDetails(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    disposable_income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Disposable income", blank=True, null=True)
    recommended_loan_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Recommended loan amount", blank=True, null=True)
    recommended_tenure = models.IntegerField(verbose_name="Recommended tenure", blank=True, null=True)
    bm_visit_done_at_business_premises = models.BooleanField(verbose_name="BM visit done at business premises",  blank=True, null=True)
    cattle_business_since = models.CharField(max_length=100, verbose_name="Cattle Business Since", blank=True, null=True)
    number_of_cattle = models.CharField(max_length=100, verbose_name="Number Of Cattle", blank=True, null=True)
    income_source_agri_land = models.CharField(max_length=100, verbose_name="Income source/agri land", blank=True, null=True)
    milk_selling_price_per_litre = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Milk selling price per litre", blank=True, null=True)
    milk_production_per_day = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Milk production per day in litre", blank=True, null=True)
    name_of_dairy_and_milk_selling_since = models.CharField(max_length=100, verbose_name="Name Of Dairy And Silk Selling Since", blank=True, null=True)
    total_household_income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total household income", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.income_source_agri_land)


class P21FiSheet(models.Model):
    # Case details
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    case_details = models.CharField(max_length=100, verbose_name="Case Details (HOD)", blank=True, null=True)
    positive_applicant_name = models.CharField(max_length=100, verbose_name="Positive Applicant name", blank=True, null=True)
    positive_co_applicant_name = models.CharField(max_length=100, verbose_name="Positive Co-Applicant name", blank=True, null=True)
    case_id = models.CharField(max_length=100, verbose_name="Case ID", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name="Address", blank=True, null=True)
    mobile = models.CharField(max_length=15, verbose_name="Mobile", blank=True, null=True)
    location = models.CharField(max_length=100, verbose_name="Location", blank=True, null=True)
    company_name = models.CharField(max_length=100, verbose_name="Company name", blank=True, null=True)
    occupation = models.CharField(max_length=100, verbose_name="Occupation", blank=True, null=True)
    verifier_emp_id = models.CharField(max_length=100, verbose_name="Verifier emp id", blank=True, null=True)
    back_office_emp_id = models.CharField(max_length=100, verbose_name="Back office emp id", blank=True, null=True)
    date_of_allocation = models.DateField(verbose_name="Date of allocation", blank=True, null=True)
    time_of_allocation = models.TimeField(verbose_name="Time of allocation", blank=True, null=True)
    date_of_report = models.DateField(verbose_name="Date of report", blank=True, null=True)
    time_of_report = models.TimeField(verbose_name="Time of report", blank=True, null=True)
    TAT_met = models.BooleanField(verbose_name="TAT met", blank=True, null=True)
    OCL_range = models.CharField(max_length=100, verbose_name="OCL range", blank=True, null=True)
    submitted_from = models.CharField(max_length=100, verbose_name="Submitted from", blank=True, null=True)
    sub_status = models.CharField(max_length=100, verbose_name="Sub status", blank=True, null=True)
    comments = models.TextField(verbose_name="Comments", blank=True, null=True)
    person_contacted = models.BooleanField(verbose_name="Person contacted",  blank=True, null=True)
    name_of_person_contacted = models.CharField(max_length=100, verbose_name="Name of person contacted", blank=True, null=True)
    # Residence details
    residence_ownership_status = models.CharField(max_length=100, verbose_name="Residence ownership status",  blank=True, null=True)
    does_applicant_stay_in_residence = models.BooleanField(verbose_name="Does the applicant stay in this residence",  blank=True, null=True)
    duration_of_stay = models.CharField(max_length=100, verbose_name="If yes duration of stay",  blank=True, null=True)
    approximate_time_when_applicant_is_available_at_home = models.CharField(max_length=100, verbose_name="Approx time when applicant is available at home", blank=True, null=True)
    number_of_person_staying_with_applicant = models.IntegerField(verbose_name="Number of person staying with applicant", blank=True, null=True)
    relationship_of_those_person_with_applicant = models.CharField(max_length=100, verbose_name="Relationship of those person with applicant", blank=True, null=True)
    prominent_landmark = models.CharField(max_length=255, verbose_name="Prominent landmark", blank=True, null=True)
    locality_of_residence = models.CharField(max_length=255, verbose_name="Locality of residence", blank=True, null=True)
    residence_accessibility = models.CharField(max_length=100, verbose_name="Residence accessibility", blank=True, null=True)
    type_of_residence = models.CharField(max_length=100, verbose_name="Type of residence", blank=True, null=True)
    external_appearance_of_house_building = models.CharField(max_length=100, verbose_name="External appearance of house/building", blank=True, null=True)
    construction_of_house = models.CharField(max_length=100, verbose_name="Construction of house", blank=True, null=True)
    carpet_area_in_sq_ft = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Carpet area in Sq. Ft.",  blank=True, null=True)
    internal_appearance_of_house = models.CharField(max_length=100, verbose_name="Internal appearance of house", blank=True, null=True)
    assets_seen_at_residence = models.CharField(max_length=255, verbose_name="Assets seen at residence", blank=True, null=True)
    political_link = models.CharField(max_length=100, verbose_name="Political link", blank=True, null=True)
    neighbour_1_name = models.CharField(max_length=100, verbose_name="Neighbour 1 name", blank=True, null=True)
    neighbour_1_status = models.CharField(max_length=100, verbose_name="Neighbour 1 Status", blank=True, null=True)
    user = models.CharField(max_length=50, verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.case_details)
