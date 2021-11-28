from django.conf import settings
from django.db import models


class Transaction(models.Model):
    transaction_name = models.ForeignKey('doctors.Speciality', related_name='transaction_for', on_delete=models.DO_NOTHING, blank=True, null=True)
    transaction_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transaction_by', on_delete=models.DO_NOTHING, blank=True, null=True)
    ref_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction details for {self.transaction_name} with ref_id: {self.ref_id}"