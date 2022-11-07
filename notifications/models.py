from django.db import models

from rides.models import Ride
from users.models import User


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        ACCEPT_REQ = "accept_req"
        REJECT_REQ = "reject_req"
        JOIN_REQ = "join_req"
        EDIT_INFO = "edit_info"
        RESIGN_INFO = "resign_info"
        CANCEL_INFO = "cancel_info"

    class RecipientType(models.TextChoices):
        DRIVER = 'driver'
        PASSENGER = 'passenger'

    notification_id = models.AutoField(primary_key=True)
    recipient_type = models.CharField(choices=RecipientType.choices, default=RecipientType.DRIVER, max_length=15)
    notification_type = models.CharField(choices=NotificationType.choices, max_length=15)
    ride = models.ForeignKey(Ride, on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Email(models.Model):
    email_id = models.AutoField(primary_key=True)
    recipient_id: int
    notification_id: int
    created_at = models.DateTimeField(auto_now_add=True)
