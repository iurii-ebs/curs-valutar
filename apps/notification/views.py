from notifications.models import Notification
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notification.serializers import NotificationSerializer


class AllNotificationsListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request):
        queryset = request.user.notifications.all()
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)


class UnreadNotificationsListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request):
        queryset = request.user.notifications.unread()
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)


class MarkAllAsRead(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request):
        request.user.notifications.mark_all_as_read()

        return Response({"text": "All notifications were marked as read."})


class MarkAsRead(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def put(self, request, pk):
        notification = get_object_or_404(Notification, recipient=request.user, id=pk)
        notification.mark_as_read()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class MarkAsUnread(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def put(self, request, pk):
        notification = get_object_or_404(Notification, recipient=request.user, id=pk)
        notification.mark_as_unread()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class DeleteNotification(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def delete(self, request, pk):
        notification = get_object_or_404(Notification, recipient=request.user, id=pk)
        notification.delete()

        return Response({"text": "Notification deleted"})


class AllNotificationsCount(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request):
        count = request.user.notifications.all().count()
        return Response({"all_count": count})


class UnreadNotificationsCount(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request):
        count = request.user.notifications.unread().count()
        return Response({"all_unread_count": count})
