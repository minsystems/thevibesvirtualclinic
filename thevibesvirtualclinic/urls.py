"""thevibesvirtualclinic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
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

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings

from thevibesvirtualclinic.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('account/', include(('accounts.urls', 'account-url'), namespace='account-url')),
    path('api/auth/', include(('accounts.api.urls', 'api-auth'), namespace='api-auth')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
