import random
import os

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from thevibesvirtualclinic.utils import unique_slug_generator

# Create your models here.

User = get_user_model()


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


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
STATE_CHOICES = (
    ('Lagos', 'Lagos'),
    ('Imo', 'Imo'),
    ('Anambra', 'Anambra'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=100, blank=True, null=True,
                            help_text="Copy This Data From Firebase UUID AccountKit")
    bio = models.TextField(blank=True, null=True)
    phone = PhoneNumberField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    image = CloudinaryField(upload_image_path, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    street = models.CharField(max_length=300, default='')
    city = models.CharField(max_length=200, default='')
    state = models.CharField(max_length=200, default='', choices=STATE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        unique_together = ('phone', 'slug')

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse('account-url:profile', kwargs={'slug': self.slug})

    @property
    def age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25)

    def image_tag(self):
        from django.utils.html import escape, mark_safe
        return mark_safe('<img src="%s" width="100" height="100" />' % self.image.url)

    image_tag.short_description = 'Profile Image'
    image_tag.allow_tags = True

    def get_address(self):
        if self.street and self.city and self.state:
            address = "{} {}, {}".format(self.street, self.city, self.state)
            return address.title()
        return "You Have Not Updated Your Profile"

    def address_tag(self):
        return self.get_address()
    address_tag.short_description = 'Next Of Kin Address'
    address_tag.allow_tags = True

    def get_name(self):
        if self.user.first_name and self.user.last_name:
            caps_initials = "{} {}".format(self.user.first_name, self.user.last_name)
            caps_initials = caps_initials.title()
            return caps_initials
        return self.user.username

    def get_firebase_id(self):
        if self.uuid:
            return self.uuid
        return "GET UUID FROM TREDES FLEETS MOBILE"

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return "https://img.icons8.com/officel/2x/user.png"


NOK_CHOICES = (
    ('Brother', 'Brother'),
    ('Sister', 'Sister'),
    ('Mom', 'Mom'),
    ('Dad', 'Dad'),
    ('Step Mom', 'Step Mom'),
    ('Step Dad', 'Step Dad'),
    ('Grand Mom', 'Grand Mom'),
    ('Grand Dad', 'Grand Dad'),
    ('Uncle', 'Uncle'),
    ('Aunty', 'Aunty'),
    ('Guardian', 'Guardian'),
    ('Friend', 'Friend'),
)


class NextOfKin(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(blank=True, null=True, max_length=200)
    last_name = models.CharField(blank=True, null=True, max_length=200)
    relationship = models.CharField(help_text="Relationship with Next Of Kin", max_length=300, default='',
                                    choices=NOK_CHOICES)
    bio = models.TextField(blank=True, null=True)
    phone = PhoneNumberField()
    street = models.CharField(max_length=300, default='')
    city = models.CharField(max_length=200, default='')
    state = models.CharField(max_length=200, default='', choices=STATE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "NextOfKin"
        verbose_name = "Informant"
        verbose_name_plural = "Informant"
        unique_together = ('phone',)

    def __str__(self):
        return str("{} {}".format(self.first_name, self.last_name))

    def get_address(self):
        if self.street and self.city and self.state:
            address = "{} {}, {}".format(self.street, self.city, self.state)
            return address.title()
        return "You Have Not Updated Your Next Of Kin Information"

    def address_tag(self):
        return self.get_address()

    address_tag.short_description = 'Next Of Kin Address'
    address_tag.allow_tags = True


def post_save_profile_receiver(sender, created, instance, *args, **kwargs):
    if created:
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)
            instance.save()

        NextOfKin.objects.get_or_create(user=instance.user, phone='')


post_save.connect(post_save_profile_receiver, sender=Profile)
