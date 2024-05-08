from django.contrib import admin

from apps.invoice.models import Invoice
# Register your models here.

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Invoice admin"""

    list_display = ["id", "cufe", "events", "issuer_name"]
    search_fields = ["cufe"]