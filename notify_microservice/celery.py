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
from rides.serializers import ParticipationSerializer
from notify_microservice.utils import create_ride, update_ride, check_and_create_user, notify_by_decision, \
    notify_of_ride_changes
from notifications.models import Notification

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
            'x-queue_rides-type': 'classic'
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
                check_and_create_user(body['message'])

        if body['title'] == 'rides.create':
            check_and_create_user(body['message']['driver'])
            create_ride(body['message'])

        if body['title'] == 'rides.create.many':
            for ride in body['message']:
                check_and_create_user(ride['driver'])
                create_ride(ride)

        if body['title'] == 'rides.update':
            check_and_create_user(body['message']['ride']['driver'])
            try:
                ride = Ride.objects.get(ride_id=body['message']['ride']['ride_id'])
                update_ride(body['message']['ride'], ride)
            except Ride.DoesNotExist:
                ride = create_ride(body['message']['ride'])

            # create notification
            notify_of_ride_changes(ride, Notification.NotificationType.EDIT_INFO)

        if body['title'] == 'rides.update.many':
            for instance in body['message']:
                check_and_create_user(body['message']['ride']['driver'])
                try:
                    ride = Ride.objects.get(ride_id=instance['ride']['ride_id'])
                    update_ride(body['message']['ride'], ride)
                except Ride.DoesNotExist:
                    ride = create_ride(instance['ride'])

                # create notification
                notify_of_ride_changes(ride, Notification.NotificationType.EDIT_INFO)

        if body['title'] == 'rides.cancel':
            check_and_create_user(body['message']['driver'])
            try:
                ride = Ride.objects.get(ride_id=body['message']['ride_id'])
                update_ride(body['message'], ride)
            except Ride.DoesNotExist:
                ride = create_ride(body['message'])

            # create notification
            notify_of_ride_changes(ride, Notification.NotificationType.CANCEL_INFO)

        if body['title'] == 'rides.cancel.many':
            for ride in body['message']:
                check_and_create_user(ride['driver'])
                try:
                    ride = Ride.objects.get(ride_id=ride['ride_id'])
                    update_ride(body['message'], ride)
                except Ride.DoesNotExist:
                    create_ride(ride)

                # create notification
                notify_of_ride_changes(ride, Notification.NotificationType.CANCEL_INFO)

        if body['title'] == 'participation':
            driver = check_and_create_user(body['message']['ride']['driver'])
            passenger = check_and_create_user(body['message']['user'])

            try:
                ride = Ride.objects.get(ride_id=body['message']['ride']['ride_id'])
                update_ride(body['message']['ride'], ride)
            except Ride.DoesNotExist:
                ride = create_ride(body['message']['ride'])

            try:
                participation = Participation.objects.get(participation_id=body['message']['id'])
                participation_data = {
                    'decision': body['message']['decision'],
                    'reserved_seats': body['message']['reserved_seats'],
                }
                serializer = ParticipationSerializer(participation, data=participation_data, partial=True)
                if serializer.is_valid():
                    serializer.save()

                    # send email notification depending on decision
                    notify_by_decision(participation_data['decision'], ride, passenger, driver, participation)

            except Participation.DoesNotExist:

                participation = Participation.objects.create(
                    participation_id=body['message']['id'],
                    decision=body['message']['decision'],
                    reserved_seats=body['message']['reserved_seats'],
                    ride_id=body['message']['ride']['ride_id'],
                    user_id=body['message']['ride']['driver']['user_id']
                )
                participation.save()

                # send email notification depending on decision
                notify_by_decision(participation.decision, ride, passenger, driver, participation)

        message.ack()


app.steps['consumer'].add(MyConsumerStep)
