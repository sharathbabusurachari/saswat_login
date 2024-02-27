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
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    mid_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    work_dept = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=15)
    designation = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    designation_id = models.CharField(max_length=10,blank=True, null=True)

#     class Meta:
#         unique_together = ('user_id', 'mobile_no')

    def __str__(self):
        return self.first_name


class UserOtp(models.Model):
    # mobile_no = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    otp_genration_time = models.DateTimeField(auto_now_add=True)
    otp_expiration_time = models.DateTimeField()

    def save(self, *args, **kwargs):

        if not self.pk:
            self.otp_expiration_time = datetime.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.otp_genration_time < timezone.now() - timezone.timedelta(minutes=2)

    # @staticmethod
    # def delete_expired():
    #     expired_otps = UserOtp.objects.filter(otp_expiration_time__lte=datetime.now())
    #     expired_otps.delete()


class GpsModel(models.Model):
    user_id = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    gps_date = models.DateField()
    gps_time = models.TimeField()
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    gender_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.gender


class State(models.Model):
    state_id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=20)

    def __str__(self):
        return self.state


class CustomerTest(models.Model):
    c_id = models.IntegerField(primary_key=True)
    c_name = models.CharField(max_length=20)
    c_dob = models.DateField()
    c_gender_id = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='customers_gender')
    c_locality = models.CharField(max_length=200)
    c_state_id = models.ForeignKey(State, on_delete=models.CASCADE, related_name='customers_state')
    c_mobile_no = models.CharField(max_length=10)
    version = models.CharField(max_length=20)
    document_name = models.CharField(max_length=20)
    document_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.c_name
