from django.contrib import admin
from django import forms
from django.db.models import F
# Register your models here.
import random

from .models import (UserDetails, UserOtp, GpsModel, CustomerTest, Gender, State,
                     VleVillageInfo, BmcBasicInformation, VleBasicInformation,
                     VleMobileNumber, PhotoOfBmc, VLEBankDetails, SkillsAndKnowledge,
                     VLEEconomicAndSocialStatusInfo,
                     VleNearbyMilkCenterContact, VillageDetails, VleOtp,VleMobileVOtp,
                     Country, District, DesignationDetails, WeekDetails,
                     EmployeeDetails, EmployeeTargetDetails, EmployeeSetTargetDetails,
                     LoanApplication, QueryModel, QnaAttachment, SignInSignOut, ShortenedQueries)


class GpsModelAdmin(admin.ModelAdmin):
    list_display = ('mobile_no', 'name', 'latitude', 'longitude', 'gps_date', 'gps_time', 'status', 'created_at')
    list_per_page = 20


admin.site.register(GpsModel, GpsModelAdmin)

admin.site.register(UserOtp)
# admin.site.register(UserDetails)
admin.site.register(CustomerTest)
admin.site.register(Gender)
# admin.site.register(State)

class VleVillageInfoAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(VleVillageInfo, VleVillageInfoAdmin)


class BmcBasicInformationAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(BmcBasicInformation, BmcBasicInformationAdmin)


class VleBasicInformationAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(VleBasicInformation, VleBasicInformationAdmin)


class VleMobileNumberAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(VleMobileNumber, VleMobileNumberAdmin)


class PhotoOfBmcAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(PhotoOfBmc, PhotoOfBmcAdmin)


class VLEBankDetailsAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(VLEBankDetails, VLEBankDetailsAdmin)


class SkillsAndKnowledgeAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(SkillsAndKnowledge, SkillsAndKnowledgeAdmin)


class VLEEconomicAndSocialStatusInfoAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(VLEEconomicAndSocialStatusInfo, VLEEconomicAndSocialStatusInfoAdmin)


class VleNearbyMilkCenterContactAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(VleNearbyMilkCenterContact, VleNearbyMilkCenterContactAdmin)


class VillageDetailsAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(VillageDetails, VillageDetailsAdmin)

class VleMobileAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(VleMobileVOtp, VleMobileAdmin)


class VleOtpAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

admin.site.register(VleOtp, VleOtpAdmin)

# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*------Dashboard API------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------


class CountryAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(Country, CountryAdmin)


class StateAdmin(admin.ModelAdmin):
    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(State, StateAdmin)


class DistrictAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(District, DistrictAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(UserDetails, UserDetailsAdmin)


class DesignationDetailsAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(DesignationDetails, DesignationDetailsAdmin)


class WeekDetailsAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Only for new instances, not for editing existing ones
            last_week = WeekDetails.objects.order_by('-week_number').first()
            if last_week:
                last_week_number = last_week.week_number
                month = last_week.month_name
                year = last_week.year
                end_date = last_week.end_date
                form.base_fields['week_number'].help_text = \
                    f'The Latest created week number is {last_week_number} for {month}, {year} (End Date - {end_date})'
        return form

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(WeekDetails, WeekDetailsAdmin)



class EmployeeDetailsAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    list_select_related = ['employee', 'designation', 'reporting_manager', 'cluster_head']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reporting_manager":
            # Filter queryset to include only employees with the designation "Reporting Manager"
            kwargs["queryset"] = EmployeeDetails.objects.filter(designation__designation_name="Reporting Manager")
        if db_field.name == "cluster_head":
            # Filter queryset to include only employees with the designation "Cluster Head"
            kwargs["queryset"] = EmployeeDetails.objects.filter(designation__designation_name="Cluster Head")


        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(EmployeeDetails, EmployeeDetailsAdmin)


class EmployeeTargetDetailsAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def has_change_permission(self, request, obj=None):
        # Prevent updating records
        return False

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(EmployeeTargetDetails,EmployeeTargetDetailsAdmin)


class EmployeeSetTargetDetailsAdmin(admin.ModelAdmin):

    exclude = ('created_by', 'modified_by')

    excluded_fields = ['month_name']

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields if field.name not in self.excluded_fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def has_change_permission(self, request, obj=None):
        # Prevent updating records
        return False

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(EmployeeSetTargetDetails,EmployeeSetTargetDetailsAdmin)

class LoanApplicationAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')
    excluded_fields = ['created_at', 'modified_at', 'created_by', 'modified_by']
    search_fields = ['saswat_application_number', 'loan_id']

    def get_model_fields(self, obj):
        fields = [field.name for field in obj._meta.fields if field.name not in self.excluded_fields]
        fields += ['get_reporting_manager_name', 'get_district', 'get_cluster']
        fields += self.excluded_fields
        return fields

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def get_reporting_manager_name(self, obj):
        return obj.sales_officer_rm

    get_reporting_manager_name.short_description = 'SO: RM name'

    def get_district(self, obj):
        return obj.sales_officer_district

    get_district.short_description = 'SO: District'

    def get_cluster(self, obj):
        return obj.sales_officer_cluster

    get_cluster.short_description = 'SO: Cluster'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sales_officer":
            kwargs["queryset"] = EmployeeDetails.objects.filter(designation__designation_name="Sales Officer")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(LoanApplication, LoanApplicationAdmin)


# class QueryAdmin(admin.ModelAdmin):
#     exclude = ('created_by', 'modified_by')
#     excluded_fields = ['id', 'saswat_application_number']
#
#     def get_model_fields(self, obj):
#         fields = ['id', 'saswat_application_number', 'get_loan_id']
#         fields += [field.name for field in obj._meta.fields if field.name not in self.excluded_fields]
#         return fields
#
#     list_display = []
#
#     def __init__(self, model, admin_site):
#         super().__init__(model, admin_site)
#         self.list_display = self.get_model_fields(model)
#
#     def get_loan_id(self, obj):
#         return obj.loan_id
#
#     get_loan_id.short_description = 'Loan ID'
#
#     def save_model(self, request, obj, form, change):
#         if not obj.created_by:
#             obj.created_by = request.user.username
#         obj.modified_by = request.user.username
#         super().save_model(request, obj, form, change)
#
#
# admin.site.register(Query, QueryAdmin)

class AttachmentOneInline(admin.TabularInline):
    model = QnaAttachment
    extra = 1
    fields = ('so_attachment', 'ta_attachment')


class MainModelOneAdmin(admin.ModelAdmin):
    inlines = [AttachmentOneInline]
    search_fields = ['saswat_application_number__saswat_application_number', 'query_status']
    exclude = ['query_id', 'created_by', 'modified_by']

    excluded_fields = ['id', 'saswat_application_number']

    def get_model_fields(self, obj):
        fields = ['id', 'saswat_application_number', 'loan_id']
        fields += [field.name for field in obj._meta.fields if field.name not in self.excluded_fields]
        return fields

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username

        if not change or not obj.query_id:
            obj.query_id = self.generate_query_id()

        existing_entries_count = QueryModel.objects.filter(
            query_id=obj.query_id
        ).annotate(
            num_entries=F('id')
        ).count()
        obj.version = existing_entries_count + 1
        obj.pk = None

        super().save_model(request, obj, form, change)

    def generate_query_id(self):
        while True:
            query_id = f"{random.randint(000000, 999999)}"
            if not QueryModel.objects.filter(query_id=query_id).exists():
                return query_id

    def get_loan_id(self, obj):
        return obj.loan_id


admin.site.register(QueryModel, MainModelOneAdmin)


@admin.register(QnaAttachment)
class QnaAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'saswat_application_number', 'so_attachment', 'ta_attachment')

    def saswat_application_number(self, obj):
        return obj.query.saswat_application_number

    saswat_application_number.short_description = 'Saswat Application Number'


class SignInSignOutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'client_id', 'event_type', 'event_date', 'event_time', 'created_at', 'remarks_one')
    # list_select_related = ['user']
    list_display_links = ('id', 'user')
    search_fields = ('user__user_id', 'user__first_name')
    search_help_text = f'Search with the User ID or First Name of User.'
    list_filter = ['event_date', 'user']


admin.site.register(SignInSignOut, SignInSignOutAdmin)

class ShortenedQueriesAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(ShortenedQueries, ShortenedQueriesAdmin)