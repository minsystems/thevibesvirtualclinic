"""tredes accounts URL Configuration
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from .views import RegisterView, LoginView, UserProfileView

urlpatterns = [
    path('sign-up/', RegisterView.as_view(), name='register'),
    path('sign-in/', LoginView.as_view(), name='login'),
    path('sign-out/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='profile'),
]
