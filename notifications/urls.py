from django.urls import path

from notifications.views import notification_list_view, notification_delete_view

urlpatterns = [
    path('', notification_list_view, name="list"),
    path('<int:pk>/delete', notification_delete_view, name="delete"),
]