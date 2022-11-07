from rides.models import Ride
from rides.serializers import RideSerializer
from users.models import User


def create_ride(message):
    try:
        User.objects.get(user_id=message['driver']['user_id'])
    except User.DoesNotExist:
        new_user = User.objects.create(
            user_id=message['driver']['user_id'],
            first_name=message['driver']['first_name'],
            last_name=message['driver']["last_name"],
            email=message['driver']["email"],
            date_of_birth=message['driver']['date_of_birth'],
            private=True if message['driver']['user_type'] == 'private' else False,
            avg_rate=message['driver']["avg_rate"],
        )
        new_user.save()

    new_ride = Ride.objects.create(
        ride_id=message['ride_id'],
        city_from=message['city_from']['name'],
        city_to=message["city_to"]['name'],
        start_date=message["start_date"],
        price=message['price'],
        driver_id=message['driver']['user_id']
    )
    new_ride.save()


def update_ride(message, ride):
    ride_data = {
        'city_from': message['city_from'],
        'city_to': message["city_to"],
        'start_date': message['start_date'],
        'price': message['price'],
    }
    serializer = RideSerializer(ride, data=ride_data, partial=True)
    if serializer.is_valid():
        serializer.save()
