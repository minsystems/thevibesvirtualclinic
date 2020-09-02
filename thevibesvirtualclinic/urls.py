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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings

from thevibesvirtualclinic.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('services/', include(('services.urls', 'consultations-url'), namespace='consultations-url')),
    path('account/', include(('accounts.urls', 'account-url'), namespace='account-url')),
    path('api/auth/', include(('accounts.api.urls', 'api-auth'), namespace='api-auth')),
    path('articles/', include(('articles.urls', 'articles'), namespace='articles')),
    path('specialties/', include(('doctors.urls', 'doctors'), namespace='doctors')),
    path('page-not-found/', TemplateView.as_view(template_name='404_.html'), name='404_'),
    path('terms_and_conditions/', TemplateView.as_view(template_name='terms_and_conditions.html'), name='t_and_c'),
]

# administrator backend service url
urlpatterns += [
    path('admin-the-vibes-virtual-clinic/', admin.site.urls),
]

#url to catch any unmatch url for 404...
urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='404_.html'))]

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
