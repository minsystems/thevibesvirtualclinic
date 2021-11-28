from django.db import models

# Create your models here.
import os
import random

from cloudinary.models import CloudinaryField
from django.db import models

# Create your models here.
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from notifications.models import Notification


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


STATUS_CHOICES = (('A', 'Active'), ('C', 'Cancelled'),)


class HospitalAliasQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def search(self, query):
        lookups = (Q(name__icontains=query) | Q(description__icontains=query))
        return self.filter(lookups).distinct()


class HospitalAliasManager(models.Manager):
    def get_queryset(self):
        return HospitalAliasQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self):
        qs = self.get_queryset().filter(id=id)
        if qs.count == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class HospitalAlias(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    image = CloudinaryField(upload_image_path, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = HospitalAliasManager()

    class Meta:
        db_table = "hospital-alias"
        verbose_name = "hospital-alias"
        verbose_name_plural = "hospital-aliases"

    def __str__(self):
        return self.name

    def image_tag(self):
        from django.utils.html import escape, mark_safe
        return mark_safe('<img src="%s" width="500" height="300" />' % self.image.url)

    image_tag.short_description = 'Hospital Logo Image'
    image_tag.allow_tags = True

    def get_absolute_url(self):
        return reverse("doctors-url:hospital-trips-doctors", kwargs={"slug": self.slug})

    @property
    def title(self):
        return self.name


DOCTOR_STATUS = (('Active', 'Active'), ('Inactive', 'Inactive'),)
DOCTOR_TYPE = (
    ('Paediatrician', 'Paediatrician'),
    ('Dentist', 'Dentist'),
    ('Neuro-Surgeon', 'Neuro-Surgeon'),
)


class DoctorsQuerySet(models.query.QuerySet):
    def condition_ok(self):
        return self.filter(condition__iexact="Active")

    def condition_bad(self):
        return self.filter(condition__iexact="Inactive")


class DoctorsManager(models.Manager):
    def get_queryset(self):
        return DoctorsQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()


class Doctors(models.Model):
    hospital_alias = models.ForeignKey(HospitalAlias, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = CloudinaryField(upload_image_path, null=True, blank=True)
    condition = models.CharField(max_length=99, choices=DOCTOR_STATUS, blank=True, null=True)
    doctor_type = models.CharField(max_length=99, choices=DOCTOR_TYPE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = DoctorsManager()

    class Meta:
        db_table = "doctors"
        verbose_name = "doctors"
        verbose_name_plural = "doctorses"

    def __str__(self):
        return "{} from {}".format(self.name, self.hospital_alias)

    def image_tag(self):
        from django.utils.html import escape, mark_safe
        return mark_safe('<img src="%s" width="500" height="300" />' % self.image.url)

    image_tag.short_description = 'Doctors Image'
    image_tag.allow_tags = True


class SpecialityCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=225, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Speciality Type"
        verbose_name_plural = "Speciality Types"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("speciality_category_detail", args=[self.name])

    def check_image_url(self):
        if self.image_url:
            return self.image_url
        return "https://res.cloudinary.com/geetechlab-com/image/upload/v1598875956/vibes_clinic/thevibesclinic1_oin5ql.jpg"

    @property
    def num_of_speciality(self):
        self.speciality_category = SpecialityCategory.objects.first()
        return self.speciality_set.all().count()


class Speciality(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    speciality_category = models.ForeignKey(SpecialityCategory, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "speciality"
        verbose_name = "speciality"
        verbose_name_plural = "specialities"

    def check_image_url(self):
        if self.image_url:
            return self.image_url
        return "https://res.cloudinary.com/geetechlab-com/image/upload/v1598875956/vibes_clinic/thevibesclinic1_oin5ql.jpg"

    def __str__(self):
        return self.name


# @receiver(post_save, sender=Speciality)
# def user_add_comment_property(sender, instance, *args, **kwargs):
#     speciality = instance
#     sender = speciality.by
#     text_preview = speciality.content[:50]
#     message = f"{speciality.by} just commented at {comm_prop.name}"
#     notify = Notification(
#         comment=comment,
#         from_user=sender,
#         to_user=comm_prop.uploaded_by.business_user,
#         text_preview=text_preview,
#         notification_type=2,
#         message=message,
#     )
#     notify.save()
