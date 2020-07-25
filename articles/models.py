import datetime
import random

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
# from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.html import mark_safe
from django.utils.text import slugify
# from markdown import markdown



def upload_dir(instance, filename):
    return "{}/{}".format(instance.author, filename)


class ArticleQuerySet(models.query.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().not_draft()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("articles_by_category", args=[self.name])


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # description = models.CharField(max_length=400)
    description = RichTextUploadingField(max_length=255, null=True)
    image = CloudinaryField(upload_dir, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=False)
    # body = models.TextField(blank=True, null=True)
    body = RichTextUploadingField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    draft = models.BooleanField(default=True)
    # published = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    objects = ArticleManager()

    class Meta:
        verbose_name_plural = "Articles"
        ordering = ('-created',)
        unique_together = ["slug", "title", ]

    def __str__(self):
        return self.title

    def image_url(self):
        if self.image:
            return self.image.url
        return 'https://res.cloudinary.com/geetechlab-com/image/upload/v1580824596/nwaben.com/blog_image1_eklmqy.jpg'

    def get_absolute_url(self):
        return reverse("articles:article_detail", kwargs={"slug": self.slug})

    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)

    # @property
    # def all_comments(self):
    #     article = Article.objects.get(slug=self.slug)
    #     return article.comment_set.all().count()
    # def get_message_as_markdown(self):
    #     return mark_safe(markdown(self.body, safe_mode='escape'))


def article_pre_save_signal(sender, instance, *args, **kwargs):
    # instance = "Second Article" -- Article title
    if not instance.slug:
        instance.slug = slugify(instance.title)
        new_slug = "{}-{}".format(instance.title, instance.id)
        # random_numbers = random.randint(1111, 9999)
        try:
            instance.slug = slugify(new_slug)
        except Article.DoesNotExist:
            instance.slug = instance.slug
        except Article.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
        except:
            pass


pre_save.connect(article_pre_save_signal, sender=Article)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def approved(self):
        self.approved = True
        self.save()

    def __str__(self):
        return '{} - {}'.format(self.content, self.by)

    # def get_comment_message_as_markdown(self):
    #     return mark_safe(markdown(self.content, safe_mode='escape'))

    #
    # def __str__(self):
    #     if self.by == None:
    #         return "ERROR-USER NAME IS NULL"
    #     return self.by

    class Meta:
        ordering = ['created_on']


class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    replied_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    replied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['replied_on']