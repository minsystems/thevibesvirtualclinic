from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db.models import Q
from django.urls import reverse

from doctors.models import Doctors

User = get_user_model()


class ConsultationsQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(from_locale__icontains=query) | Q(to_locale__icontains=query) | Q(doctor__icontains=query))
        return self.filter(lookups).distinct()


class ConsultationsManager(models.Manager):
    def get_queryset(self):
        return ConsultationsQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self):
        qs = self.get_queryset().filter(id=id)
        if qs.count == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Consultations(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=5000)
    active = models.BooleanField(default=True)
    consultation_time = models.DateTimeField(blank=True, null=True)
    ticket_key = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ConsultationsManager()

    class Meta:
        db_table = "consultations"
        verbose_name = "consultations"
        verbose_name_plural = "consultations"
        ordering = ("-timestamp",)

    def __str__(self):
        return self.doctor

    def get_absolute_url(self):
        return reverse("consultations-url:consultation-detail", kwargs={"slug": self.slug})


class Services(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "services"
        verbose_name = "services"
        verbose_name_plural = "services"
        ordering = ("-timestamp",)

    def __str__(self):
        return self.name
