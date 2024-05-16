from django.contrib import admin
from django import forms

# Register your models here.

from .models import (UserDetails, UserOtp, GpsModel, CustomerTest, Gender, State,
                     VleVillageInfo, BmcBasicInformation, VleBasicInformation,
                     VleMobileNumber, PhotoOfBmc, VLEBankDetails, SkillsAndKnowledge,
                     VLEEconomicAndSocialStatusInfo,
                     VleNearbyMilkCenterContact, VillageDetails, VleOtp,VleMobileVOtp,
                     Country, District, DesignationDetails, WeekDetails,
                     EmployeeDetails, EmployeeTargetDetails, EmployeeSetTargetDetails)

admin.site.register(UserOtp)
# admin.site.register(UserDetails)
admin.site.register(GpsModel)
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


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # return "Category: {}".format(obj.name)
        if obj.mid_name is None or obj.mid_name == "":
            return "{} {}_{}".format(obj.first_name, obj.last_name, obj.user_id)
        elif obj.last_name is None or obj.last_name == "":
            return "{} {}_{}".format(obj.first_name, obj.mid_name, obj.user_id)
        elif (obj.mid_name is None or obj.mid_name == "") and (obj.last_name is None or obj.last_name == ""):
            return "{}_{}".format(obj.first_name, obj.user_id)
        else:
            return "{} {} {}_{}".format(obj.first_name, obj.mid_name, obj.last_name, obj.user_id)


class EmployeeDetailsAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by')

    def get_model_fields(self, obj):
        return [field.name for field in obj._meta.fields]

    list_display = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_model_fields(model)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reporting_manager":
            # Filter queryset to include only employees with the designation "Reporting Manager"
            kwargs["queryset"] = EmployeeDetails.objects.filter(designation__designation_name="Reporting Manager")
        if db_field.name == "cluster_head":
            # Filter queryset to include only employees with the designation "Cluster Head"
            kwargs["queryset"] = EmployeeDetails.objects.filter(designation__designation_name="Cluster Head")
        if db_field.name == 'employee':
            return UserChoiceField(queryset=UserDetails.objects.all())

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
