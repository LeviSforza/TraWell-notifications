import json
import os
from datetime import date

from app.mail.templates import HTML_BODY_USER, HTML_BODY_RIDE, CSS_STYLE
from app.models.notification import NotificationType
from app.models.ride import RideInDB
from app.models.ride_passenger import RidePassengerInDB
from app.models.user import UserInDB
from dotenv import load_dotenv
from redmail import gmail


def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def read_json():
    with open("app/mail/mail_options.json", "r") as f:
        msg_types = json.load(f)
    return msg_types


mail_options = read_json()
load_dotenv()


def send_mail_user(notification_type: NotificationType, requester: UserInDB, receiver: UserInDB, ride_passenger: RidePassengerInDB):
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
                "logo": 'app/mail/images/logo_bg_round.png',
                "picture": f'app/mail/images/{setup_info["picture"]}.png',
            },
            body_params={
                'css': CSS_STYLE,
                'title': setup_info['title'],
                'content': setup_info['content'],
                'message': setup_info['message'],
                'box_color': setup_info['box_color'],
                'name': requester.first_name,
                'age': age(requester.date_of_birth),
                'avg_rate': str(requester.avg_rate),
                'seats': ride_passenger.seats
            }
        )
        return True

    except ConnectionError:
        print("Error occured during sending mail")

    return False


def send_mail_ride(notification_type: NotificationType, sender: UserInDB, receiver: UserInDB, ride: RideInDB):
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
                "logo": 'app/mail/images/logo_bg_round.png',
                "picture": f'app/mail/images/{setup_info["picture"]}.png',
            },
            body_params={
                'css': CSS_STYLE,
                'title': setup_info['title'],
                'content': setup_info['content'],
                'message': setup_info['message'],
                'box_color': setup_info['box_color'],
                'city_from': ride.city_from,
                'city_to': ride.city_to,
                'ride_date': ride.start_date.date(),
                'ride_time': str(ride.start_date.hour) + ':' + str(ride.start_date.minute),
                'price': ride.price,
                'driver': sender.first_name
            }
        )
        return True

    except ConnectionError:
        print("Error occured during sending mail")

    return False
