from django.db import models

from users.models import User


# Create your models here.

class Ride(models.Model):
    ride_id = models.AutoField(primary_key=True)
    city_from = models.CharField(max_length=100, blank=True, default="")
    city_to = models.CharField(max_length=100, blank=True, default="")
    start_date = models.DateTimeField(null=False)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    driver = models.ForeignKey(User, related_name='driver', on_delete=models.SET_NULL, blank=False, null=True)
    passengers = models.ManyToManyField(User, blank=True, through='Participation')


class Participation(models.Model):
    class Decision(models.TextChoices):
        ACCEPTED = 'accepted'
        DECLINED = 'declined'
        PENDING = 'pending'
        CANCELLED = 'cancelled'

    participation_id = models.AutoField(primary_key=True)
    ride = models.ForeignKey(Ride, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, related_name='passenger', on_delete=models.SET_NULL, null=True)
    decision = models.CharField(choices=Decision.choices, default=Decision.PENDING, max_length=9)
    reserved_seats = models.IntegerField(default=1, blank=False, null=False)

