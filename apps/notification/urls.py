from django.urls import path, re_path

from apps.notification import views

urlpatterns = [
    path('notifications/all/', views.AllNotificationsListView.as_view(), name='all_notifications'),
    path('notifications/unread/', views.UnreadNotificationsListView.as_view(), name='unread_notifications'),
    path('notifications/mark-all-as-read/', views.MarkAllAsRead.as_view(), name='mark_all_as_read_notifications'),
    path('notifications/mark-as-read/<int:pk>/', views.MarkAsRead.as_view(), name='mark_as_read_notification'),
    path('notifications/mark-as-unread/<int:pk>/', views.MarkAsUnread.as_view(), name='mark_as_unread_notification'),
    path('notifications/delete/<int:pk>/', views.DeleteNotification.as_view(), name='delete_notification'),
    path('notifications/unread_count/', views.UnreadNotificationsCount.as_view(), name='live_unread_notifications_count'),
    path('notifications/all_count/', views.AllNotificationsCount.as_view(), name='live_all_notifications_count'),
]
