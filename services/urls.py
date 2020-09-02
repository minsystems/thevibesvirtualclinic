from django.urls import path

from services.views import ConsultationsList, ConsultationsDetails, ConsultationsSearchResultView, ServiceList

urlpatterns = [
    path('', ConsultationsList.as_view(), name='consultations-list'),
    path('services-listings/', ServiceList.as_view(), name='service-list'),
    path('result/', ConsultationsSearchResultView.as_view(), name='consultations-result'),
    path('<slug:slug>/details/', ConsultationsDetails.as_view(), name='consultations-detail'),
]