from django.db import models
from django.contrib import admin
from .models import Article, Comment, Category, Reply

# from pagedown.widgets import AdminPagedownWidget
# Register your models here.

admin.site.register(Category)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created', 'category')
    list_filter = ('author', 'created', 'created', 'category')
    search_field = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}


# formfield_overrides = {
#     models.TextField: {'widget': AdminPagedownWidget },
# }
admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('by', 'content', 'approved')


admin.site.register(Comment, CommentAdmin)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('replied_by', 'content')


admin.site.register(Reply, ReplyAdmin)