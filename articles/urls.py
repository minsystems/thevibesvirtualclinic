from django.urls import path
from articles import views

# from .forms import ArticleForm

urlpatterns = [
    path('details/<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('', views.ArticleList.as_view(), name='article_list'),
]