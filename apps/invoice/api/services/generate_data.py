import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.invoice.api.serializers import InvoiceSerializer
from apps.invoice.api.services.scrapper import DIANScraper
from apps.invoice.models import Invoice

class InvoiceService:
    """Handler class for Invoice"""

    def __init__(self) -> None:
        self.scrapper = DIANScraper()


    def save_invoice_data(self, cufe) -> dict:        
        """ function to save the invoice data to the database """
        try:
            data_scrapper = self.scrapper.scrape_invoice_data(cufe)
            invoice_data = {
                "cufe": cufe,
                "events": data_scrapper["invoice_events"],
                "issuer_name": data_scrapper["datos"]["DATOS DEL EMISOR Nombre"],
                "issuer_nit": data_scrapper["datos"]["DATOS DEL EMISOR NIT"],
                "receiver_name": data_scrapper["datos"]["DATOS DEL RECEPTOR Nombre"],
                "receiver_nit": data_scrapper["datos"]["DATOS DEL RECEPTOR NIT"],
                "representation": data_scrapper["graphic_representation"],
            }
            invoice, created = Invoice.objects.get_or_create(cufe=cufe, defaults=invoice_data)
            if created:
                print(f"Invoice with CUFE {cufe} successfully saved.")
            else:
                print(f"Invoice with CUFE {cufe} already exists in the database. Skipping...")
        except Exception as e:
            print(f"Error processing CUFE {cufe}: {e}")
    
    def save_invoice_data_for_cufes(self, cufes):
        """ function that calls the function to store each invoice """
        for cufe in cufes:
            self.save_invoice_data(cufe)
    
    def get_all_invoices_data(self):
        """ Function to fetch all invoices and serialize them. """
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return serializer.data

    def build_invoice_data_response(self, cufes):
        """ Function that is called from the view to execute the scrapper and return the invoices."""
        self.save_invoice_data_for_cufes(cufes)
        invoices = self.get_all_invoices_data()
        return invoices
    


