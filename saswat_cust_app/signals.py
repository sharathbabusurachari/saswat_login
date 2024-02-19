from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserOtp

@receiver(pre_save, sender=UserOtp)
def delete_expired_otps(sender, instance, **kwargs):
    if instance.is_expired():
        instance.delete()
