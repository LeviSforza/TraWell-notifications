from rest_framework import serializers

from notifications.models import Notification, Mail
from rides.serializers import RideSerializer
from users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    ride = RideSerializer(many=False)

    class Meta:
        model = Notification
        fields = ('notification_id', 'recipient_type', 'notification_type', 'ride', 'sender', 'created_at')


class EmailSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    notification = NotificationSerializer(many=False)

    class Meta:
        model = Mail
        fields = ('email_id', 'recipient', 'notification', 'created_at')
