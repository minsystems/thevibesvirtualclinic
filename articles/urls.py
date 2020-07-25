from django.urls import path
from articles import views

# from .forms import ArticleForm

urlpatterns = [
    # path('category/create', views.CategoryCreate.as_view(), name='category_create'),
    # path('category/<int:pk>', views.ArticleCategory.as_view(), name='article_category'),
    # path('delete/<slug:slug>', views.ArticleDelete.as_view(), name='article_delete'),
    # path('update/<slug:slug>', views.ArticleUpdate.as_view(), name='article_update'),
    # path('dashboard/', views.DashBoard.as_view(), name='article_dashboard'),
    # path('create/', views.ArticleCreate.as_view(), name='article_create'),
    path('details/<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('', views.ArticleList.as_view(), name='article_list'),
]