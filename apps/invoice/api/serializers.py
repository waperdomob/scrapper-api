from rest_framework import serializers
from apps.invoice.models import Invoice


class EventSerializer(serializers.Serializer):
    eventNumber = serializers.CharField(source='Código')
    eventName = serializers.CharField(source='Descripción')

class InvoiceSerializer(serializers.ModelSerializer):
    events = serializers.JSONField()
    sellerInformation = serializers.SerializerMethodField()
    receiverInformation = serializers.SerializerMethodField()
    linkGraphicRepresentation = serializers.CharField(source='representation')

    class Meta:
        model = Invoice
        fields = ('cufe', 'events', 'sellerInformation', 'receiverInformation', 'linkGraphicRepresentation')

    def get_sellerInformation(self, obj):
        return {
            "Document": obj.issuer_nit,
            "Name": obj.issuer_name
        }

    def get_receiverInformation(self, obj):
        return {
            "Document": obj.receiver_nit,
            "Name": obj.receiver_name
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        events_data = data.pop('events', [])
        events = EventSerializer(events_data, many=True).data
        data['events'] = events
        return data

class RequestSerializer(serializers.Serializer):
    cufes = serializers.ListField(child=serializers.CharField())

    def to_internal_value(self, data):
        """Function to clean up the blanks by removing the blanks"""
        if 'cufes' in data:
            cleaned_cufes = [cufe.strip() for cufe in data['cufes']]
            data['cufes'] = cleaned_cufes
        return super().to_internal_value(data)