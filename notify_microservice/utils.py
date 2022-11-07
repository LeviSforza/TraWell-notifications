from mail.utils_mail import send_mail_ride, send_mail_user
from notifications.models import Notification, Mail
from rides.models import Ride, Participation
from rides.serializers import RideSerializer, RideUpdateSerializer
from users.models import User


def create_ride(message):
    new_ride = Ride.objects.create(
        ride_id=message['ride_id'],
        city_from=message['city_from']['name'],
        city_to=message["city_to"]['name'],
        start_date=message["start_date"],
        price=message['price'],
        driver_id=message['driver']['user_id']
    )
    new_ride.save()
    return new_ride


def update_ride(message, ride):
    ride_data = {
        'city_from': message['city_from'],
        'city_to': message["city_to"],
        'start_date': message['start_date'],
        'price': message['price'],
    }
    serializer = RideUpdateSerializer(ride, data=ride_data, partial=True)
    if serializer.is_valid():
        serializer.save()


def check_and_create_user(message):
    try:
        user = User.objects.get(user_id=message['user_id'])
    except User.DoesNotExist:
        user = User.objects.create(
            user_id=message['user_id'],
            first_name=message['first_name'],
            last_name=message["last_name"],
            email=message["email"],
            date_of_birth=message['date_of_birth'],
            private=True if message['user_type'] == 'private' else False,
            avg_rate=message["avg_rate"],
        )
        user.save()
    return user


def notify_by_decision(decision: Notification.NotificationType, ride: Ride, passenger: User, driver: User, participation: Participation):
    if decision == Participation.Decision.ACCEPTED:
        notification = Notification.objects.create(
            recipient_type=Notification.RecipientType.PASSENGER,
            notification_type=Notification.NotificationType.ACCEPT_REQ,
            ride=ride,
            sender=ride.driver
        )
        notification.save()

        send_mail_ride(
            Notification.NotificationType.ACCEPT_REQ,
            sender=driver,
            receiver=passenger,
            ride=ride)

        email = Mail.objects.create(
            recipient=participation.user,
            notification=notification
        )
        email.save()

    if decision == Participation.Decision.DECLINED:
        notification = Notification.objects.create(
            recipient_type=Notification.RecipientType.PASSENGER,
            notification_type=Notification.NotificationType.REJECT_REQ,
            ride=ride,
            sender=ride.driver
        )
        notification.save()

        send_mail_ride(
            Notification.NotificationType.REJECT_REQ,
            sender=driver,
            receiver=passenger,
            ride=ride)

        email = Mail.objects.create(
            recipient=participation.user,
            notification=notification
        )
        email.save()

    if decision == Participation.Decision.CANCELLED:
        notification = Notification.objects.create(
            recipient_type=Notification.RecipientType.DRIVER,
            notification_type=Notification.NotificationType.RESIGN_INFO,
            ride=ride,
            sender=passenger
        )
        notification.save()

        send_mail_user(
            Notification.NotificationType.RESIGN_INFO,
            sender=passenger,
            receiver=driver,
            participation=participation)

        email = Mail.objects.create(
            recipient=driver,
            notification=notification
        )
        email.save()

    if decision == Participation.Decision.PENDING:
        notification = Notification.objects.create(
            recipient_type=Notification.RecipientType.DRIVER,
            notification_type=Notification.NotificationType.RESIGN_INFO,
            ride=ride,
            sender=passenger
        )
        notification.save()

        send_mail_user(
            Notification.NotificationType.JOIN_REQ,
            sender=passenger,
            receiver=driver,
            participation=participation)

        email = Mail.objects.create(
            recipient=driver,
            notification=notification
        )
        email.save()


def notify_of_ride_changes(ride: Ride, notification_type: Notification.NotificationType):
    notification = Notification.objects.create(
        recipient_type=Notification.RecipientType.PASSENGER,
        notification_type=notification_type,
        ride=ride,
        sender=ride.driver
    )
    notification.save()

    # send email notification - cancel info
    participations = Participation.objects.all().filter(ride=ride)
    for participation in participations:
        send_mail_ride(
            notification_type=notification_type,
            sender=ride.driver,
            receiver=participation.user,
            ride=ride)

        email = Mail.objects.create(
            recipient=participation.user,
            notification=notification
        )
        email.save()
