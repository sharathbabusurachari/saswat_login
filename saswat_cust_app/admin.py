from django.contrib import admin
from django import forms
from django.db.models import F, Q
# Register your models here.
import random
from .forms import QueryModelForm

from .models import (UserDetails, UserOtp, GpsModel, CustomerTest, Gender, State,
                     VleVillageInfo, BmcBasicInformation, VleBasicInformation,
                     VleMobileNumber, PhotoOfBmc, VLEBankDetails, SkillsAndKnowledge,
                     VLEEconomicAndSocialStatusInfo,
                     VleNearbyMilkCenterContact, VillageDetails, VleOtp,VleMobileVOtp,
                     Country, District, DesignationDetails, WeekDetails,
                     EmployeeDetails, EmployeeTargetDetails, EmployeeSetTargetDetails,
                     LoanApplication, QueryModel, QnaAttachment, SignInSignOut, ShortenedQueries, QueryDocuments, ESign)
from django.http import HttpResponse
import csv
from openpyxl import Workbook
from django.utils.text import slugify


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action.
    'fields' and 'exclude' work like in ModelForm
    'header' is whether or not to output the column names as the first row
    """

    def export_as_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]

        if fields:
            fieldset = set(fields)
            field_names = [f for f in field_names if f in fieldset]


        if exclude:
            excludeset = set(exclude)
            field_names = [f for f in field_names if f not in excludeset]

        # Create the response object and set the headers
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={slugify(opts.verbose_name_plural)}.csv'

        # Create a CSV writer object
        writer = csv.writer(response)

        # Write the header row
        if header:
            writer.writerow(field_names)

        # Write data rows
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)

        return response

    export_as_csv.short_description = description
    return export_as_csv


def export_as_excel_action(description="Export selected objects as Excel file",
                           fields=None, exclude=None, header=True):
    def export_as_excel(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]

        if fields:
            fieldset = set(fields)
            field_names = [f for f in field_names if f in fieldset]

        if exclude:
            excludeset = set(exclude)
            field_names = [f for f in field_names if f not in excludeset]

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={slugify(opts.verbose_name_plural)}.xlsx'

        wb = Workbook()
        ws = wb.active

        if header:
            ws.append(field_names)

        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field)
                # Convert any non-primitive values to strings
                if not isinstance(value, (str, int, float, bool, type(None))):
                    value = str(value)
                row.append(value)
            ws.append(row)

        wb.save(response)
        return response

    export_as_excel.short_description = description
    return export_as_excel


class GpsModelAdmin(admin.ModelAdmin):
    list_display = ('mobile_no', 'name', 'latitude', 'longitude', 'gps_date', 'gps_time', 'status', 'remarks',
                    'created_at')
    list_per_page = 20
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(GpsModel, GpsModelAdmin)


admin.site.register(CustomerTest)
admin.site.register(Gender)
# admin.site.register(State)


class UserOtpAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)


admin.site.register(UserOtp, UserOtpAdmin)


class VleVillageInfoAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]
    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(VleVillageInfo, VleVillageInfoAdmin)


class BmcBasicInformationAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(BmcBasicInformation, BmcBasicInformationAdmin)


class VleBasicInformationAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(VleBasicInformation, VleBasicInformationAdmin)


class VleMobileNumberAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(VleMobileNumber, VleMobileNumberAdmin)


class PhotoOfBmcAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(PhotoOfBmc, PhotoOfBmcAdmin)


class VLEBankDetailsAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(VLEBankDetails, VLEBankDetailsAdmin)


class SkillsAndKnowledgeAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(SkillsAndKnowledge, SkillsAndKnowledgeAdmin)


class VLEEconomicAndSocialStatusInfoAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(VLEEconomicAndSocialStatusInfo, VLEEconomicAndSocialStatusInfoAdmin)


class VleNearbyMilkCenterContactAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(VleNearbyMilkCenterContact, VleNearbyMilkCenterContactAdmin)


class VillageDetailsAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(VillageDetails, VillageDetailsAdmin)

class VleMobileAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(VleMobileVOtp, VleMobileAdmin)


class VleOtpAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(State, StateAdmin)


class DistrictAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(UserDetails, UserDetailsAdmin)


class DesignationDetailsAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    actions = [export_as_csv_action(), export_as_excel_action()]

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
            kwargs["queryset"] = EmployeeDetails.objects.filter(Q(designation__designation_name="Sales Officer") |
                                                                Q(designation__designation_name="Reporting Manager")
                                                                )
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
    form = QueryModelForm
    inlines = [AttachmentOneInline]
    search_fields = ['saswat_application_number__saswat_application_number', 'query_status']
    exclude = ['query_id', 'created_by', 'modified_by']
    excluded_fields = ['id', 'saswat_application_number', ]

    def get_model_fields(self, obj):
        fields = ['id', 'saswat_application_number', 'loan_id']
        fields += [field.name for field in obj._meta.fields if field.name not in self.excluded_fields]
        return fields

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]

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
    list_display = ('id', 'query_id', 'so_attachment', 'ta_attachment', 'remarks')
    actions = [export_as_csv_action(), export_as_excel_action()]

    def saswat_application_number(self, obj):
        return obj.query.query_id

    saswat_application_number.short_description = 'Saswat Application Number'


class SignInSignOutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'client_id', 'event_type', 'event_date', 'event_time', 'created_at', 'remarks',
                    'remarks_one')
    # list_select_related = ['user']
    list_display_links = ('id', 'user')
    search_fields = ('user__user_id', 'user__first_name')
    search_help_text = f'Search with the User ID or First Name of User.'
    list_filter = ['event_date', 'user']
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(SignInSignOut, SignInSignOutAdmin)

class ShortenedQueriesAdmin(admin.ModelAdmin):

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)
    actions = [export_as_csv_action(), export_as_excel_action()]


admin.site.register(ShortenedQueries, ShortenedQueriesAdmin)


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'document_name', 'created_at']


admin.site.register(QueryDocuments, DocumentsAdmin)


class ESignAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')
    list_display = (
        'id', 'user', 'customer_mobile_number', 'customer_name', 'file_name', 'file', 's_file_data_base64',
        's_validate_login_api_response', 's_embedded_signing_api_response', 'esign_status',
        'remarks', 'created_at', 'modified_at', 'created_by', 'modified_by'
    )
    # list_select_related = ['user']
    list_per_page = 30
    actions = [export_as_csv_action(), export_as_excel_action()]
    list_display_links = ('id', 'user')
    search_fields = ('user__user_id', 'user__first_name', 'customer_mobile_number')
    search_help_text = f'Search with the User ID or First Name of User or Mobile Number of Customer.'
    list_filter = ['created_at', 'user', 'customer_mobile_number']

    def truncate_field(self, field_value, max_length=30):
        return (str(field_value)[:25] + '.....') if len(str(field_value)) > max_length else field_value

    def get_truncated_field_method(field_name, short_description):
        def method(self, obj):
            return self.truncate_field(getattr(obj, field_name))
        method.short_description = short_description
        return method
    s_file_data_base64 = get_truncated_field_method('file_data_base64', 'BASE 64 DATA OF FILE')
    s_validate_login_api_response = get_truncated_field_method('validate_login_api_response',
                                                               'VALIDATE LOGIN API RESPONSE')
    s_embedded_signing_api_response = get_truncated_field_method('embedded_signing_api_response',
                                                                 'EMBEDDED SIGNIN API RESPONSE')

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(ESign, ESignAdmin)