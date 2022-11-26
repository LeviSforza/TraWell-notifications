import json
import logging
import os
from datetime import date
from dotenv import load_dotenv
from redmail import gmail

from mail.templates import HTML_BODY_USER, CSS_STYLE, HTML_BODY_RIDE
from notifications.models import Notification, Mail
from rides.models import Ride, Participation
from users.models import User


def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def read_json():
    with open("./mail/mail_options.json", "r") as f:
        msg_types = json.load(f)
    return msg_types


mail_options = read_json()
load_dotenv()


def send_mail_user(notification_type: Notification.NotificationType, sender: User,
                   receiver: User, participation: Participation):
    gmail.username = os.getenv('EMAIL_ADDRESS')
    gmail.password = os.getenv('EMAIL_PASSWORD')

    setup_info = mail_options[notification_type]

    try:
        gmail.send(
            subject=setup_info['subject'],
            receivers=[receiver.email],
            text=setup_info['content'],
            html=HTML_BODY_USER,
            body_images={
                "logo": './mail/images/logo_bg_round.png',
                "picture": f'./mail/images/{setup_info["picture"]}.png',
            },
            body_params={
                'css': CSS_STYLE,
                'title': setup_info['title'],
                'content': setup_info['content'],
                'message': setup_info['message'],
                'box_color': setup_info['box_color'],
                'name': sender.first_name,
                'age': age(sender.date_of_birth),
                'avg_rate': str(sender.avg_rate),
                'seats': participation.reserved_seats
            }
        )
        return True

    except ConnectionError:
        print("Error occurred during sending mail")
        logging.error("Error occurred during sending mail")

    return False


def send_mail_ride(notification_type: Notification.NotificationType, sender: User,
                   receiver: User, ride: Ride):
    gmail.username = os.getenv('EMAIL_ADDRESS')
    gmail.password = os.getenv('EMAIL_PASSWORD')

    setup_info = mail_options[notification_type]

    try:
        gmail.send(
            subject=setup_info['subject'],
            receivers=[receiver.email],
            text=setup_info['content'],
            html=HTML_BODY_RIDE,
            body_images={
                "logo": './mail/images/logo_bg_round.png',
                "picture": f'./mail/images/{setup_info["picture"]}.png',
            },
            body_params={
                'css': CSS_STYLE,
                'title': setup_info['title'],
                'content': setup_info['content'],
                'message': setup_info['message'],
                'box_color': setup_info['box_color'],
                'city_from': ride.city_from,
                'city_to': ride.city_to,
                'ride_date': str(ride.start_date)[:10],
                'ride_time': str(ride.start_date.hour) + ':' + str(ride.start_date.minute),
                'price': ride.price,
                'driver': sender.first_name
            }
        )
        return True

    except ConnectionError:
        print("Error occurred during sending mail")
        logging.error("Error occurred during sending mail")

    return False
