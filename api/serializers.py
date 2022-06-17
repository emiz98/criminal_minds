from rest_framework import serializers

from .models import Investigation, InvestigationData


class InvestigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigation
        fields = '__all__'


class InvestigationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestigationData
        fields = '__all__'
