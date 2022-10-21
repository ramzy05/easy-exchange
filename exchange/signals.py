from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Account
from .utils import get_random_pin


@receiver(pre_save, sender=Account)
def generate_code_pin(sender, instance, *args, **kwargs):
    code_pin = get_random_pin()
    instance.pin = code_pin
