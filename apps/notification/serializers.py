from notifications.models import Notification
from rest_framework import serializers
from apps.notification.models import CustomContentType


class NotificationSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = ('id', 'unread', 'recipient', 'verb', 'level', 'content_type', 'target_object_id', 'timestamp',)

    def get_content_type(self, obj):
        queryset = CustomContentType.objects.get(id=obj.action_object_object_id)
        return queryset.type
