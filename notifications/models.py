from django.conf import settings
from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Transaction_message'),
    )
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_to', on_delete=models.CASCADE, blank=True, null=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_from', on_delete=models.CASCADE, blank=True, null=True)
    from_admin = models.CharField(max_length=100, blank=True, null=True, default="System Notification")
    speciality = models.ForeignKey('doctors.Speciality', related_name='speciality_notifications', on_delete=models.CASCADE, blank=True, null=True)
    text_preview = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.to_user} initiated transaction for {self.speciality.name} Price: {self.speciality.price}..."