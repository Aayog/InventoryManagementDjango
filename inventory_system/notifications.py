from django.core.mail import send_mail
from django.conf import settings
from .models import Product

def check_inventory_and_send_email():
    # Check inventory levels
    low_stock_items = Product.objects.filter(stock__lte=settings.LOW_STOCK_THRESHOLD)
    
    if low_stock_items:
        # Prepare email content
        subject = 'Low Stock Notification'
        message = 'The following items are running low in stock: \n\n'
        for item in low_stock_items:
            message += f'{item.name}: {item.stock} remaining\n'
        
        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.NOTIFICATION_EMAIL],
            fail_silently=False,
        )

