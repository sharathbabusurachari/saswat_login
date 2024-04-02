from django.contrib import admin
# from django.apps import apps
from django.contrib.auth.models import User

from data_entry_app.models import (P01BusinessLoanAppForm, P02FinancialRequirement, P03Applicant,
                                   P04BankAccountDetail, P05CustomerConsent, P06GstDeclaration, P07ReferenceOne,
                                   P08ReferenceTwo, P09CoApplicant, P10Attachment, P11PostDatedCheques,
                                   P12SequrityPostDatedCheques, P13SpdcAndPdcForm, P14PdSheetPersonalDetails,
                                   P15PdBusinessDetails, P16PdLoanDetails, P17PdTotalAssets, P18PdVisit,
                                   P19PdBureauSummary, P21FiSheet, P20PdMiscellaneousDetails,
                                   P22InsuranceApplicationToAmbit, P23InsuranceApplicationToSaswat)


# models = apps.get_models()
#
# for model in models:
#     try:
#         admin.site.register(model)

#     except admin.sites.AlreadyRegistered:
#         pass

from django.db import models
from django.contrib.auth.models import User


class P01BusinessLoanAppFormAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)  # Save


admin.site.register(P01BusinessLoanAppForm, P01BusinessLoanAppFormAdmin)


class P02FinancialRequirementAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P02FinancialRequirement, P02FinancialRequirementAdmin)


class P03ApplicantAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P03Applicant, P03ApplicantAdmin)


class P04BankAccountDetailAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P04BankAccountDetail, P04BankAccountDetailAdmin)


class P05CustomerConsentAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P05CustomerConsent, P05CustomerConsentAdmin)


class P06GstDeclarationAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P06GstDeclaration, P06GstDeclarationAdmin)


class P07ReferenceOneAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P07ReferenceOne, P07ReferenceOneAdmin)


class P08ReferenceTwoAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P08ReferenceTwo, P08ReferenceTwoAdmin)


class P09CoApplicantAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P09CoApplicant, P09CoApplicantAdmin)


class P10AttachmentAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P10Attachment, P10AttachmentAdmin)


class P11PostDatedChequesAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P11PostDatedCheques, P11PostDatedChequesAdmin)


class P12SequrityPostDatedChequesAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P12SequrityPostDatedCheques, P12SequrityPostDatedChequesAdmin)


class P13SpdcAndPdcFormAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P13SpdcAndPdcForm, P13SpdcAndPdcFormAdmin)


class P14PdSheetPersonalDetailsAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P14PdSheetPersonalDetails, P14PdSheetPersonalDetailsAdmin)


class P15PdBusinessDetailsAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P15PdBusinessDetails, P15PdBusinessDetailsAdmin)


class P16PdLoanDetailsAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P16PdLoanDetails, P16PdLoanDetailsAdmin)


class P17PdTotalAssetsAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P17PdTotalAssets, P17PdTotalAssetsAdmin)


class P18PdVisitAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P18PdVisit, P18PdVisitAdmin)


class P19PdBureauSummaryAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P19PdBureauSummary, P19PdBureauSummaryAdmin)


class P20PdMiscellaneousDetailsAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P20PdMiscellaneousDetails, P20PdMiscellaneousDetailsAdmin)


class P21FiSheetAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P21FiSheet, P21FiSheetAdmin)


class P22InsuranceApplicationToAmbitAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P22InsuranceApplicationToAmbit, P22InsuranceApplicationToAmbitAdmin)


class P23InsuranceApplicationToSaswatAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(P23InsuranceApplicationToSaswat, P23InsuranceApplicationToSaswatAdmin)
