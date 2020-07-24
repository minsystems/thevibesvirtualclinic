from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token # accounts app

from .views import AuthAPIView, RegisterAPIView

urlpatterns = [
    path('', AuthAPIView.as_view(), name='login-api'),
    path('register/', RegisterAPIView.as_view(), name='register-api'),
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),
]