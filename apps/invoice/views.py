from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from apps.invoice.api.services.generate_data import InvoiceService
from apps.invoice.models import Invoice
from apps.invoice.api.serializers import InvoiceSerializer, RequestSerializer

# Create your views here.

class InvoiceApiView(APIView):
    """Conjunto de vistas para el modelo Invoice."""

    def __init__(self) -> None:
        self.instance = InvoiceService()

    
    def post(self, request):
        """ Method Post to send cufes and get invoices """
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            cufes = self.instance.build_invoice_data_response(serializer.validated_data['cufes'])            
            return Response({"cufes": cufes}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    