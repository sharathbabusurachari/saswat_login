from django.contrib import admin

# Register your models here.

from .models import UserDetails, UserOtp, GpsModel


admin.site.register(UserOtp)
admin.site.register(UserDetails)
admin.site.register(GpsModel)
