from django.db import models


# Create your models here.
class BusinessLoanAppForm(models.Model):
    app_no = models.CharField(verbose_name="Application No", max_length=10, primary_key=True)
    app_date = models.DateField(verbose_name="Application Date")
    city = models.CharField(max_length=50, verbose_name="City")

    def __str__(self):
        return self.app_no


class FinancialRequirement(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    purpose_of_loan = models.CharField(max_length=50, verbose_name="Purpose of loan")
    loan_type = models.CharField(max_length=50, verbose_name="Application Date")
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan amount")
    desire_tenure = models.IntegerField(verbose_name="Desire Tenure")

    def __str__(self):
        return self.purpose_of_loan


class CoApplicant(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    father_or_spouse_name = models.CharField(max_length=100, verbose_name="Father/Spouse's Name")
    pan_number = models.CharField(max_length=10, verbose_name="PAN No")
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15, verbose_name="Mobile")
    email = models.EmailField(max_length=100, verbose_name="E-mail")
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


class BankAccountDetail(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=11, verbose_name="IFSC code")
    account_number = models.CharField(max_length=20)
    micr_code = models.CharField(max_length=9, verbose_name="MICR code")

    def __str__(self):
        return f"{self.account_name}'s {self.bank_name} Account"


class CustomerConsent(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    applied_amount = models.DecimalField(max_digits=12, decimal_places=2,verbose_name="Applied Amount INR")

    def __str__(self):
        return f"Applied Amount: ₹{self.applied_amount}"


# class KycDeclaration(models.Model):
#     kyc_declaration_of_applicants = models.BooleanField(verbose_name="KYC Declaration of Applicants")
#     kyc_declaration_of_co_applicants = models.BooleanField(verbose_name="KYC Declaration of Co-Applicants")
#
#     def __str__(self):
#         return f"KYC Declaration of - {self.id}"


class GstDeclaration(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=100)

    def __str__(self):
        return f"GST Declaration - Applicant: {self.applicant_name}"


class ReferenceOne(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    contact_details = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ReferenceTwo(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    contact_details = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Applicant(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    father_or_spouse_name = models.CharField(max_length=100, verbose_name="Father/Spouse's Name")
    pan_number = models.CharField(max_length=10, verbose_name="PAN No")
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15, verbose_name="Mobile")
    email = models.EmailField(max_length=100, verbose_name="E-mail")
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


class InsuranceApplicationToSaswat(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField()
    loan_facility = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan facility (Rs)")
    insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Insurance premium (Rs)")
    to_specified_paravet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To specified Paravet (Rs)")

    def __str__(self):
        return f"Details - {self.date}"


class InsuranceApplicationToAmbit(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date")
    loan_facility = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Loan facility (Rs)")
    insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Insurance premium (Rs)")
    to_specified_paravet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To specified Paravet (Rs)")

    def __str__(self):
        return f"Details - {self.date}"


class Attachment(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    applicant_adhaar = models.FileField(upload_to='attachments/', verbose_name="Applicant Adhaar(Masked and signed-OSV)")
    applicant_pan = models.FileField(upload_to='attachments/', verbose_name="Applicant PAN(Signed-OSV)")
    applicant_form_sixty = models.FileField(upload_to='attachments/', verbose_name="Applicant Form-60(Signed-OSV)"
                                                                                 "(if no PAN)")
    applicant_voter_id = models.FileField(upload_to='attachments/', verbose_name="Applicant Voter  Id(Optional)")
    co_applicant_adhaar = models.FileField(upload_to='attachments/', verbose_name="Co-Applicant Adhaar(Masked and signed)")
    co_applicant_pan = models.FileField(upload_to='attachments/', verbose_name="Co-Applicant PAN(Signed)")
    bankers_verification = models.FileField(upload_to='attachments/', verbose_name="Bankers Verification")
    indemnity_bond_signature = models.FileField(upload_to='attachments/', verbose_name="Indemnity bond - signature /name/dob(With notorized affidavit)")
    milk_statement = models.FileField(upload_to='attachments/', verbose_name="Milk statement")
    bank_statement = models.FileField(upload_to='attachments/', verbose_name="Bank statement")
    living_certificate = models.FileField(upload_to='attachments/', verbose_name="Living certificate")
    nach_mandate = models.FileField(upload_to='attachments/', verbose_name="NACH Mandate")
    spdc_pdc_cheques = models.FileField(upload_to='attachments/', verbose_name="SPDC/PDC Cheques(Applicant & co-applicant)")
    address_proof = models.FileField(upload_to='attachments/', verbose_name="Address proof(ration card, electricity bill, pahani, gas cylender book, etc..)")
    anexure = models.FileField(upload_to='attachments/', verbose_name="Anexure")
    vernacular_signature = models.FileField(upload_to='attachments/', verbose_name="Vernacular Signature")
    ndc_checklist = models.FileField(upload_to='attachments/', verbose_name="NDC Checklist")
    login_checklist = models.FileField(upload_to='attachments/', verbose_name="LoginChecklist")
    loan_agreement = models.FileField(upload_to='attachments/', verbose_name="LOAN Agreement")
    audit_trail = models.FileField(upload_to='attachments/', verbose_name="Audit Trail")
    loan_deduction_table = models.FileField(upload_to='attachments/', verbose_name="Loan deduction Table")
    insurance = models.FileField(upload_to='attachments/', verbose_name="Insurance")
    field_visit_photo = models.FileField(upload_to='attachments/', verbose_name="Field visit photo(Home, cattle,shed)")
    cam_sheet = models.FileField(upload_to='attachments/', verbose_name="CAM sheet")


class SequrityPostDatedCheques(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    cheque_no_from = models.IntegerField(verbose_name="Cheque Number From")
    cheque_no_to = models.IntegerField(verbose_name="Cheque Number To")
    Amount = models.DecimalField(max_digits=12, decimal_places=2)
    issuing_bank_name = models.CharField(max_length=30, verbose_name="Issuing bank name")
    issuing_bank_ac_no = models.CharField(max_length=30, verbose_name="Issuing bank Acc Number")

    def __str__(self):
        return self.issuing_bank_name


class PostDatedCheques(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    cheque_no_from = models.IntegerField(verbose_name="Cheque Number From")
    cheque_no_to = models.IntegerField(verbose_name="Cheque Number To")
    Amount = models.DecimalField(max_digits=12, decimal_places=2)
    issuing_bank_name = models.CharField(max_length=30, verbose_name="Issuing bank name")
    issuing_bank_ac_no = models.CharField(max_length=30, verbose_name="Issuing bank Acc Number")

    def __str__(self):
        return self.issuing_bank_name


class SpdcAndPdcForm(models.Model):
    app_no = models.ForeignKey(BusinessLoanAppForm, on_delete=models.CASCADE)
    date = models.DateField()
    loan_agreement_dated = models.DateField()
    name_of_borrower_or_co_borrower = models.CharField(max_length=30, verbose_name="Name of borrower/co-borrower")

    def __str__(self):
        return self.name_of_borrower_or_co_borrower
