from django.contrib import admin

# Register your models here.

from .models import UserDetails, UserOtp, GpsModel, CustomerTest, Gender, State


admin.site.register(UserOtp)
admin.site.register(UserDetails)
admin.site.register(GpsModel)
admin.site.register(CustomerTest)
admin.site.register(Gender)
admin.site.register(State)
