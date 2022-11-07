from rest_framework import serializers

from rides.models import Ride, Participation
from users.serializers import UserSerializer


class RideSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Ride
        fields = ('ride_id', 'city_from', 'city_to', 'start_date', 'price', 'driver')


class RideUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('ride_id', 'city_from', 'city_to', 'start_date', 'price')


class ParticipationSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Participation
        fields = ('participation_id', 'ride', 'user', 'decision', 'reserved_seats')

