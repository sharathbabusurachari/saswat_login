from django.contrib import admin

# Register your models here.

from .models import (UserDetails, UserOtp, GpsModel, CustomerTest, Gender, State,
                     VleVillageInfo, BmcBasicInformation, VleBasicInformation,
                     VleMobileNumber, PhotoOfBmc, VLEBankDetails, SkillsAndKnowledge,
                     VLEEconomicAndSocialStatusInfo,
                     VleNearbyMilkCenterContact, VillageDetails)


admin.site.register(UserOtp)
admin.site.register(UserDetails)
admin.site.register(GpsModel)
admin.site.register(CustomerTest)
admin.site.register(Gender)
admin.site.register(State)

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