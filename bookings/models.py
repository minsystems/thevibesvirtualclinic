from django.contrib.auth import get_user_model
from django.db import models

from services.models import Consultations

User = get_user_model()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultations, on_delete=models.CASCADE, blank=True, null=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    token = models.CharField(max_length=200, blank=True, null=True)
    doctor = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booking"
        verbose_name = "booking"
        verbose_name_plural = "bookings"
        ordering = ('-timestamp',)

    def __str__(self):
        return "Consultation Between {} and {}".format(self.user, self.doctor)
