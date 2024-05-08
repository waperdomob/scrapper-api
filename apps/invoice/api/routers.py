from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.invoice.views import InvoiceApiView

router = DefaultRouter()


urlpatterns = [
    path('invoice/', InvoiceApiView.as_view(), name='invoice'),
]