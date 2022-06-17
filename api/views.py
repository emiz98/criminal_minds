from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import InvestigationDataSerializer, InvestigationSerializer
from .models import Investigation, InvestigationData


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Get All Investigations': '/get_investigations',
        'Get Investigation by ID': '/get_investigation/<int:id>',
        'Create Investigation': '/create_investigation',
        'Get All Investigation Data': '/get_investigation_data/<int:id>'
    }

    return Response(api_urls)


@api_view(['GET'])
def GetAllInvestigations(request):
    investigations = Investigation.objects.all().order_by('created_at').reverse()
    serializer = InvestigationSerializer(investigations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def GetInvestigation(request, pk):
    investigation = Investigation.objects.get(id=pk)
    serializer = InvestigationSerializer(investigation, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def CreateInvestigation(request):
    serializer = InvestigationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def GetInvestigationData(request, investigationId):
    investigationData = InvestigationData.objects.filter(
        investigation_id=investigationId)
    serializer = InvestigationDataSerializer(investigationData, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetInvestigationDataByCallType(request, call_type):
    investigationData = InvestigationData.objects.filter(
        call_type=call_type)
    serializer = InvestigationDataSerializer(investigationData, many=True)
    return Response(serializer.data)
