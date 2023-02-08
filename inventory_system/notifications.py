from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Product

@receiver(post_save, sender=Product)
def check_inventory_and_send_email()(sender, instance, **kwargs):
    print("Called check inventory",end="\n\n")
    # Check inventory levels
    if instance.stock < instance.stock_threshold:
        # Prepare email content
        subject = f'Stock Low Alert for {instance.name}'
        message = f'The stock for {instance.name} is low. The current stock is {instance.stock}.'
        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.NOTIFICATION_EMAIL],
            fail_silently=False,
        )