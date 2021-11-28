from django.urls import path
from .views import TransactionListView

urlpatterns = [
    path('', TransactionListView.as_view(), name="list"),
]