from django.contrib import admin

# Register your models here.

from .models import UserDetails,UserOtp


admin.site.register(UserOtp)
admin.site.register(UserDetails)