import datetime
import os
import random
import string

from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    """
    This is for a Django project with an key field
    """
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(ticket_key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_order_id_generator(instance):
    """
    This is for a Django project with an order_id field
    """
    order_new_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.phone)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))

def create_slug(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.title)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug