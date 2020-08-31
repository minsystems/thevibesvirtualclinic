from django.urls import path
from doctors import views

# from .forms import ArticleForm

urlpatterns = [
    # path('details/<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('', views.SpecialtyListView.as_view(), name='specialty_list'),
]