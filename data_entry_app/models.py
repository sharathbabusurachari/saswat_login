from django.db import models


# Create your models here.
class P01BusinessLoanAppForm(models.Model):
    app_no = models.CharField(verbose_name="Application No", max_length=10, primary_key=True)
    app_date = models.DateField(verbose_name="Application Date")
    city = models.CharField(max_length=50, verbose_name="City")

    def __str__(self):
        return self.app_no


class P02FinancialRequirement(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    purpose_of_loan = models.CharField(max_length=50, verbose_name="Purpose of loan")
    loan_type = models.CharField(max_length=50, verbose_name="Loan Type")
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan amount")
    desire_tenure = models.IntegerField(verbose_name="Desire Tenure")

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
    pan_number = models.CharField(max_length=10, verbose_name="PAN No", blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15, verbose_name="Mobile")
    email = models.EmailField(max_length=100, verbose_name="E-mail", blank=True)
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

    def __str__(self):
        return self.name


class P04BankAccountDetail(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=11, verbose_name="IFSC code")
    account_number = models.CharField(max_length=20)
    micr_code = models.CharField(max_length=9, verbose_name="MICR code", blank=True)

    def __str__(self):
        return f"{self.account_name}'s {self.bank_name} Account"


class P05CustomerConsent(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    applied_amount = models.DecimalField(max_digits=12, decimal_places=2,verbose_name="Applied Amount INR")

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

    def __str__(self):
        return f"GST Declaration - Applicant: {self.applicant_name}"


class P07ReferenceOne(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    contact_details = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class P08ReferenceTwo(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    contact_details = models.CharField(max_length=100)

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
    pan_number = models.CharField(max_length=10, verbose_name="PAN No", blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15, verbose_name="Mobile")
    email = models.EmailField(max_length=100, verbose_name="E-mail", blank=True)
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

    def __str__(self):
        return self.name


class P23InsuranceApplicationToSaswat(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField()
    loan_facility = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan facility (Rs)")
    insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Insurance premium (Rs)")
    to_specified_paravet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To specified Paravet (Rs)")

    def __str__(self):
        return f"Details - {self.date}"


class P22InsuranceApplicationToAmbit(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date")
    loan_facility = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan facility (Rs)")
    insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Insurance premium (Rs)")
    to_specified_paravet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To specified Paravet (Rs)")

    def __str__(self):
        return f"Details - {self.date}"


class P10Attachment(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    applicant_adhaar = models.FileField(upload_to='attachments/', verbose_name="Applicant Adhaar(Masked and signed-OSV)")
    # applicant_pan = models.FileField(upload_to='attachments/', verbose_name="Applicant PAN(Signed-OSV)")
    applicant_pan_or_form_sixty = models.FileField(upload_to='attachments/', verbose_name="Applicant PAN/Form 60")
    applicant_voter_id = models.FileField(upload_to='attachments/', verbose_name="Applicant Voter  Id(Optional)", blank=True)
    co_applicant_adhaar = models.FileField(upload_to='attachments/', verbose_name="Co-Applicant Adhaar(Masked and signed)")
    # co_applicant_pan = models.FileField(upload_to='attachments/', verbose_name="Co-Applicant PAN(Signed)")
    co_applicant_pan_or_form_sixty = models.FileField(upload_to='attachments/', verbose_name="Co Applicant PAN/Form 60")
    bankers_verification = models.FileField(upload_to='attachments/', verbose_name="Bankers Verification", blank=True)
    indemnity_bond_signature = models.FileField(upload_to='attachments/', verbose_name="Indemnity bond - signature /name/dob(With notorized affidavit)", blank=True)
    milk_statement = models.FileField(upload_to='attachments/', verbose_name="Milk statement")
    bank_statement = models.FileField(upload_to='attachments/', verbose_name="Bank statement")
    living_certificate = models.FileField(upload_to='attachments/', verbose_name="Living certificate", blank=True)
    nach_mandate = models.FileField(upload_to='attachments/', verbose_name="NACH Mandate")
    spdc_pdc_cheques = models.FileField(upload_to='attachments/', verbose_name="SPDC/PDC Cheques(Applicant & co-applicant)")
    address_proof = models.FileField(upload_to='attachments/', verbose_name="Address proof(ration card, electricity bill, pahani, gas cylender book, etc..)")
    anexure = models.FileField(upload_to='attachments/', verbose_name="Anexure", blank=True)
    vernacular_signature = models.FileField(upload_to='attachments/', verbose_name="Vernacular Signature", blank=True)
    ndc_checklist = models.FileField(upload_to='attachments/', verbose_name="NDC Checklist")
    login_checklist = models.FileField(upload_to='attachments/', verbose_name="LoginChecklist")
    loan_agreement = models.FileField(upload_to='attachments/', verbose_name="LOAN Agreement",blank=True)
    audit_trail = models.FileField(upload_to='attachments/', verbose_name="Audit Trail", blank=True)
    loan_deduction_table = models.FileField(upload_to='attachments/', verbose_name="Loan deduction Table", blank=True)
    insurance = models.FileField(upload_to='attachments/', verbose_name="Insurance", blank=True)
    field_visit_home = models.FileField(upload_to='attachments/', verbose_name="Field visit photo (Home)", blank=True)
    field_visit_cattle = models.FileField(upload_to='attachments/', verbose_name="Field visit photo (cattle)", blank=True)
    field_visit_shed = models.FileField(upload_to='attachments/', verbose_name="Field visit photo (shed)", blank=True)
    cam_sheet = models.FileField(upload_to='attachments/', verbose_name="CAM sheet")
    other = models.FileField(upload_to='attachments/', verbose_name="Other Attachment", blank=True)


class P12SequrityPostDatedCheques(models.Model):
    app_no = models.ForeignKey(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    cheque_no_from = models.IntegerField(verbose_name="Cheque Number From")
    cheque_no_to = models.IntegerField(verbose_name="Cheque Number To")
    Amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    issuing_bank_name = models.CharField(max_length=30, verbose_name="Issuing bank name")
    issuing_bank_ac_no = models.CharField(max_length=30, verbose_name="Issuing bank Acc Number")

    def __str__(self):
        return self.issuing_bank_name


class P11PostDatedCheques(models.Model):
    app_no = models.ForeignKey(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    cheque_no_from = models.IntegerField(verbose_name="Cheque Number From",)
    cheque_no_to = models.IntegerField(verbose_name="Cheque Number To")
    Amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    issuing_bank_name = models.CharField(max_length=30, verbose_name="Issuing bank name")
    issuing_bank_ac_no = models.CharField(max_length=30, verbose_name="Issuing bank Acc Number")

    def __str__(self):
        return self.issuing_bank_name


class P13SpdcAndPdcForm(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField()
    loan_agreement_dated = models.DateField()
    name_of_borrower_or_co_borrower = models.CharField(max_length=30, verbose_name="Name of borrower/co-borrower")

    def __str__(self):
        return self.name_of_borrower_or_co_borrower

####################

class P14PdSheetPersonalDetails(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, verbose_name="Name of customer")
    customer_date_of_birth = models.DateField(verbose_name="Date of birth of customer")
    customer_age = models.IntegerField(verbose_name="Age of customer")
    customer_kyc_source = models.CharField(max_length=100, verbose_name="KYC source of customer")

    co_applicant_name = models.CharField(max_length=100, verbose_name="Name of co-applicant")
    co_applicant_date_of_birth = models.DateField(verbose_name="Date of birth of co-applicant")
    co_applicant_age = models.IntegerField(verbose_name="Age of co-applicant")
    co_applicant_kyc_source = models.CharField(max_length=100, verbose_name="KYC source of co-applicant")

    total_dependents = models.IntegerField(verbose_name="Total Number of dependents")
    adults_count = models.IntegerField(verbose_name="Adults count")
    children_count = models.IntegerField(verbose_name="Children count")

    residence_address = models.CharField(max_length=255, verbose_name="Residence address")
    OWNED_RENTED_CHOICES = [
        ('Owned', 'Owned'),
        ('Rented', 'Rented'),
    ]
    residence_owned_rented = models.CharField(max_length=10, choices=OWNED_RENTED_CHOICES, verbose_name="Owned/rented")
    residence_stability_years = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Residence stability in years")
    kyc_source = models.CharField(max_length=100, verbose_name="KYC source")

    def __str__(self):
        return f"{self.customer_name}'s Personal Details"


class P15PdBusinessDetails(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    business_address = models.CharField(max_length=255, verbose_name="Business address")
    OWNED_RENTED_CHOICES = [
        ('Owned', 'Owned'),
        ('Rented', 'Rented'),
    ]
    business_owned_rented = models.CharField(max_length=10, choices=OWNED_RENTED_CHOICES, verbose_name="Owned/rented")
    business_stability_at_present_address_years = models.DecimalField(max_digits=12, decimal_places=2, blank=True, verbose_name="Business stability at present address in years")
    total_business_stability_years = models.DecimalField(max_digits=12, decimal_places=2, blank=True, verbose_name="Total business stability in years")
    total_experience_in_business_line_years = models.DecimalField(max_digits=12, decimal_places=2,blank=True, verbose_name="Total experience in business line in years")

    def __str__(self):
        return f"Business Details at {self.business_address}"


class P16PdLoanDetails(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    nature_of_business = models.CharField(max_length=255, verbose_name="Nature of business")
    loan_type = models.CharField(max_length=100, verbose_name="Loan type")
    applied_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Applied amount")
    applied_tenure = models.CharField(max_length=255, verbose_name="Applied tenure")
    comfortable_emi = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Comfortable EMI as per customer")
    # BORROWER_TYPE_CHOICES = [
    #     ('Individual', 'Individual'),
    #     ('Company', 'Company'),
    # ]
    borrower_type = models.CharField(max_length=100, verbose_name="Borrower type")

    def __str__(self):
        return f"Loan Details for {self.nature_of_business}"


class P17PdTotalAssets(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    home = models.CharField(max_length=255, verbose_name="Home")
    business = models.CharField(max_length=255, verbose_name="Business")
    agri_land = models.CharField(max_length=255, verbose_name="Agri land")
    additional_income = models.CharField(max_length=255, verbose_name="Additional income (others)", blank=True)

    def __str__(self):
        return self.business



class P18PdVisit(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    # reference_check_visit = models.BooleanField(verbose_name="Reference check/visit", default=False)
    residential_house_visit = models.BooleanField(verbose_name="Residential house visit", default=False)
    residential_visit_done_by = models.CharField(max_length=100, verbose_name="Done by (Residential house visit)")
    business_premises_visit = models.BooleanField(verbose_name="Business premises visit", default=False)
    business_visit_done_by = models.CharField(max_length=100, verbose_name="Done by (Business premises visit)")

    def __str__(self):
        return self.residential_visit_done_by


class P19PdBureauSummary(models.Model):
    # MFI Loan details
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    mfi_loan_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type MFI Loan amount", blank=True)
    mfi_loan_tenure = models.IntegerField(verbose_name="Loan Type MFI Loan tenure", blank=True)
    mfi_emi_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type MFI EMI amount", blank=True)
    mfi_emi_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type MFI EMI paid", blank=True)
    mfi_emi_remaining = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type MFI EMI remaining", blank=True)

    # KCC Loan details
    kcc_loan_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type KCC Loan amount", blank=True)
    kcc_loan_tenure = models.IntegerField(verbose_name="Loan Type KCC Loan tenure", blank=True)
    kcc_emi_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type KCC EMI amount", blank=True)
    kcc_emi_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type KCC EMI paid", blank=True)
    kcc_emi_remaining = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type KCC EMI remaining", blank=True)

    # Personal Loan details
    personal_loan_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Personal Loan amount", blank=True)
    personal_loan_tenure = models.IntegerField(verbose_name="Loan Type Personal Loan tenure", blank=True)
    personal_emi_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Personal Loan EMI amount", blank=True)
    personal_emi_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Personal Loan EMI paid", blank=True)
    personal_emi_remaining = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Personal Loan EMI remaining", blank=True)

    # Tractor Loan details
    tractor_loan_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Tractor Loan amount", blank=True)
    tractor_loan_tenure = models.IntegerField(verbose_name="Loan Type Tractor Loan tenure", blank=True)
    tractor_emi_amt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Tractor Loan EMI amount", blank=True)
    tractor_emi_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Tractor Loan EMI paid", blank=True)
    tractor_emi_remaining = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan Type Tractor Loan EMI remaining", blank=True)

    def __str__(self):
        return self.mfi_loan_amt


class P20PdMiscellaneousDetails(models.Model):
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    disposable_income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Disposable income",blank=True)
    recommended_loan_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Recommended loan amount")
    recommended_tenure = models.IntegerField(verbose_name="Recommended tenure")
    bm_visit_done_at_business_premises = models.BooleanField(verbose_name="BM visit done at business premises")
    income_source_agri_land = models.CharField(max_length=100, verbose_name="Income source/agri land")
    milk_selling_price_per_litre = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Milk selling price per litre")
    milk_production_per_day = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Milk production per day in litre")
    total_household_income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total household income")

    def __str__(self):
        return self.income_source_agri_land


class P21FiSheet(models.Model):
    # Case details
    app_no = models.OneToOneField(P01BusinessLoanAppForm, on_delete=models.CASCADE)
    case_details = models.CharField(max_length=100, verbose_name="Case Details (HOD)")
    positive_applicant_name = models.CharField(max_length=100, verbose_name="Positive Applicant name")
    positive_co_applicant_name = models.CharField(max_length=100, verbose_name="Positive Co-Applicant name")
    case_id = models.CharField(max_length=100, verbose_name="Case ID")
    address = models.CharField(max_length=255, verbose_name="Address")
    mobile = models.CharField(max_length=15, verbose_name="Mobile")
    location = models.CharField(max_length=100, verbose_name="Location")
    company_name = models.CharField(max_length=100, verbose_name="Company name")
    occupation = models.CharField(max_length=100, verbose_name="Occupation")
    verifier_emp_id = models.CharField(max_length=100, verbose_name="Verifier emp id")
    back_office_emp_id = models.CharField(max_length=100, verbose_name="Back office emp id", blank=True, null=True)
    date_of_allocation = models.DateField(verbose_name="Date of allocation", blank=True, null=True)
    time_of_allocation = models.TimeField(verbose_name="Time of allocation", blank=True, null=True)
    date_of_report = models.DateField(verbose_name="Date of report", blank=True, null=True)
    time_of_report = models.TimeField(verbose_name="Time of report", blank=True, null=True)
    TAT_met = models.BooleanField(verbose_name="TAT met")
    OCL_range = models.CharField(max_length=100, verbose_name="OCL range")
    submitted_from = models.CharField(max_length=100, verbose_name="Submitted from")
    sub_status = models.CharField(max_length=100, verbose_name="Sub status")
    comments = models.TextField(verbose_name="Comments")
    person_contacted = models.BooleanField(verbose_name="Person contacted")
    name_of_person_contacted = models.CharField(max_length=100, verbose_name="Name of person contacted")
    # Residence details
    residence_ownership_status = models.CharField(max_length=100, verbose_name="Residence ownership status")
    does_applicant_stay_in_residence = models.BooleanField(verbose_name="Does the applicant stay in this residence")
    duration_of_stay = models.CharField(max_length=100, verbose_name="If yes duration of stay")
    approximate_time_when_applicant_is_available_at_home = models.CharField(max_length=100, verbose_name="Approx time when applicant is available at home")
    number_of_person_staying_with_applicant = models.IntegerField(verbose_name="Number of person staying with applicant")
    relationship_of_those_person_with_applicant = models.CharField(max_length=100, verbose_name="Relationship of those person with applicant")
    prominent_landmark = models.CharField(max_length=255, verbose_name="Prominent landmark")
    locality_of_residence = models.CharField(max_length=255, verbose_name="Locality of residence")
    residence_accessibility = models.CharField(max_length=100, verbose_name="Residence accessibility")
    type_of_residence = models.CharField(max_length=100, verbose_name="Type of residence")
    external_appearance_of_house_building = models.CharField(max_length=100, verbose_name="External appearance of house/building")
    construction_of_house = models.CharField(max_length=100, verbose_name="Construction of house")
    carpet_area_in_sq_ft = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Carpet area in Sq. Ft.")
    internal_appearance_of_house = models.CharField(max_length=100, verbose_name="Internal appearance of house")
    assets_seen_at_residence = models.CharField(max_length=255, verbose_name="Assets seen at residence")
    political_link = models.CharField(max_length=100, verbose_name="Political link")
    neighbour_1_name = models.CharField(max_length=100, verbose_name="Neighbour 1 name")
    neighbour_1_status = models.CharField(max_length=100, verbose_name="Neighbour 1 Status")

    def __str__(self):
        return self.case_details
