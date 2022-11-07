from rest_framework import serializers

from notifications.models import Notification, Email


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('notification_id', 'recipient_type', 'notification_type', 'ride', 'sender', 'created_at')


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('email_id', 'recipient_id', 'notification_id', 'created_at')
