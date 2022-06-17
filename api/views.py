from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import InvestigationDataSerializer, InvestigationSerializer
from .models import Investigation, InvestigationData
import tabula as tab


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Get All Investigations': '/get_investigations',
        'Get Investigation by ID': '/get_investigation/<int:id>',
        'Create Investigation': '/create_investigation',
        'Get All Investigation Data': '/get_investigation_data/<int:investigationId>',
        'Get All Investigation Data By Call Type': '/get_investigation_data_by_call_type/<int:call_type>',
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
    pdf = tab.read_pdf(request.data['pdf'].file, pages='all')
    print(pdf)
    serializer = InvestigationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def GetInvestigationData(request, investigationId):
    investigationData = InvestigationData.objects.filter(
        investigation_id=1)
    serializer = InvestigationDataSerializer(investigationData, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def GetInvestigationDataByCallType(request, call_type):
    investigationData = InvestigationData.objects.filter(
        call_type=call_type)
    serializer = InvestigationDataSerializer(investigationData, many=True)
    return Response(serializer.data)
