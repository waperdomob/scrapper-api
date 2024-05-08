from django.db import models

# Create your models here.
class Invoice(models.Model):
    cufe = models.CharField(max_length=100, unique=True)
    events = models.JSONField("Eventos de la factura")
    issuer_name = models.CharField("Nombre del emisor", max_length=50)
    issuer_nit = models.CharField("Nit del emisor", max_length=50)
    receiver_name = models.CharField("Nombre del receptor", max_length=50)
    receiver_nit = models.CharField("Nit del receptor", max_length=50)
    representation = models.CharField("Link de representación Grafica", max_length=255)


    def __str__(self) -> str:
        return str(self.cufe)