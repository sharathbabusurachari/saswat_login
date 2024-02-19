# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number


class UserDetails(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=20)
    mid_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    work_dept = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=15)
    designation = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    designation_id = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.first_name


class UserOtp(models.Model):
    # mobile_no = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    otp_genration_time = models.DateTimeField(auto_now_add=True)
    otp_expiration_time = models.DateTimeField()

    def __str__(self):
        return self.mobile_no

    def save(self, *args, **kwargs):

        if not self.pk:
            self.otp_expiration_time = datetime.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)


    def is_expired(self):
        return self.otp_expiration_time < timezone.now()

    # @staticmethod
    # def delete_expired():
    #     expired_otps = UserOtp.objects.filter(otp_expiration_time__lte=datetime.now())
    #     expired_otps.delete()


