from __future__ import absolute_import, unicode_literals

import os

import django
import kombu
from celery import Celery, bootsteps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notify_microservice.settings')
django.setup()

from users.models import User
from users.serializers import UserSerializer
from rides.models import Ride, Participation
from rides.serializers import RideSerializer, ParticipationSerializer
from notify_microservice.utils import create_ride, update_ride

app = Celery('notify_microservice')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# setting publisher
with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='trawell_exchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    queue = kombu.Queue(
        name='notifications',
        exchange=exchange,
        routing_key='notify',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()


# setting consumer
class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[queue],
                               callbacks=[self.handle_message],
                               accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        print(message)

        if body['title'] == 'users':
            try:
                user = User.objects.get(user_id=body['message']['user_id'])
                user_data = {
                    'first_name': body['message']['first_name'],
                    'last_name': body['message']["last_name"],
                    'date_of_birth': body['message']['date_of_birth'],
                    'avg_rate': body['message']['avg_rate'],
                }
                serializer = UserSerializer(user, data=user_data, partial=True)
                if serializer.is_valid():
                    serializer.save()

            except User.DoesNotExist:
                new_user = User.objects.create(
                    user_id=body['message']['user_id'],
                    first_name=body['message']['first_name'],
                    last_name=body['message']["last_name"],
                    email=body['message']["email"],
                    date_of_birth=body['message']['date_of_birth'],
                    private=True if body['message']['user_type'] == 'private' else False,
                    avg_rate=body['message']["avg_rate"],
                )
                new_user.save()

        if body['title'] == 'rides.create':
            create_ride(body['message'])

        if body['title'] == 'rides.create.many':
            for ride in body['message']:
                create_ride(ride)

        if body['title'] == 'rides.update':
            try:
                ride = Ride.objects.get(ride_id=body['message']['ride']['ride_id'])
                update_ride(body['message'], ride)
            except Ride.DoesNotExist:
                create_ride(body['message'])

        if body['title'] == 'rides.update.many':
            for ride in body['message']:
                try:
                    instance = Ride.objects.get(ride_id=ride['ride']['ride_id'])
                    update_ride(body['message'], instance)
                except Ride.DoesNotExist:
                    create_ride(ride)

        if body['title'] == 'rides.cancel':
            try:
                ride = Ride.objects.get(ride_id=body['message']['ride']['ride_id'])
                update_ride(body['message'], ride)
            except Ride.DoesNotExist:
                create_ride(body['message'])

        if body['title'] == 'rides.cancel.many':
            for ride in body['message']:
                try:
                    instance= Ride.objects.get(ride_id=ride['ride']['ride_id'])
                    update_ride(body['message'], instance)
                except Ride.DoesNotExist:
                    create_ride(ride)

        if body['title'] == 'participation':
            try:
                participation = Participation.objects.get(participation_id=body['message']['id'])
                participation_data = {
                    'decision': body['message']['decision'],
                }
                serializer = ParticipationSerializer(participation, data=participation_data, partial=True)
                if serializer.is_valid():
                    serializer.save()

            except Participation.DoesNotExist:
                try:
                    User.objects.get(user_id=body['message']['ride']['driver']['user_id'])
                except User.DoesNotExist:
                    new_user = User.objects.create(
                        user_id=body['message']['ride']['driver']['user_id'],
                        first_name=body['message']['ride']['driver']['first_name'],
                        last_name=body['message']['ride']['driver']["last_name"],
                        email=body['message']['ride']['driver']["email"],
                        date_of_birth=body['message']['ride']['driver']['date_of_birth'],
                        private=True if body['message']['ride']['driver']['user_type'] == 'private' else False,
                        avg_rate=body['message']['ride']['driver']["avg_rate"],
                    )
                    new_user.save()

                try:
                    Ride.objects.get(ride_id=body['message']['ride']['ride_id'])
                except Ride.DoesNotExist:
                    new_ride = Ride.objects.create(
                        ride_id=body['message']['ride']['ride_id'],
                        city_from=body['message']['ride']['city_from']['name'],
                        city_to=body['message']['ride']["city_to"]['name'],
                        start_date=body['message']['ride']["start_date"],
                        price=body['message']['ride']['price'],
                        driver_id=body['message']['ride']['driver']['user_id']
                    )
                    new_ride.save()

                new_participation = Participation.objects.create(
                    participation_id=body['message']['id'],
                    decision=body['message']['decision'],
                    reserved_seats=body['message']['reserved_seats'],
                    ride_id=body['message']['ride']['ride_id'],
                    user_id=body['message']['ride']['driver']['user_id']
                )
                new_participation.save()

        message.ack()


app.steps['consumer'].add(MyConsumerStep)
