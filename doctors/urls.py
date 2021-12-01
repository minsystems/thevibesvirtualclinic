from django.urls import path
from doctors import views

# from .forms import ArticleForm

urlpatterns = [
    path('all/', views.SpecialityListView.as_view(), name='speciality_list'),
    path('', views.SpecialityCategoryList.as_view(), name='speciality_category_List'),
    path('promo/<slug:slug>/', views.PromoNotification.as_view(), name='promo_notification'),
    path('<slug:slug>/', views.SpecialityCategoryDetail.as_view(), name='speciality_category_detail'),
    path('promo/<slug>/<speciality_pk>', views.PromoNotification.as_view(), name='promo_notification'),
]

