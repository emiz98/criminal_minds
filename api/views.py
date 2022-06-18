from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count, Sum
from .serializers import InvestigationDataSerializer, InvestigationSerializer
from .models import Investigation, InvestigationData
import tabula as tab


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Get All Investigations': '/get_investigations',
        'Get Investigation by ID': '/get_investigation/{id}',
        'Create Investigation': '/create_investigation',
        'Delete Investigation': '/delete_investigation/{id}',

        'Get Investigation Data': '/get_investigation_data/{id}',
        'Get Investigation Additional Data': '/get_investigation_additional/{call_id}/{investigation_id}',
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
def DeleteInvestigation(request, investigationId):
    investigation = Investigation.objects.get(id=investigationId)
    investigation.delete()
    return Response("Investigation deleted successfully!")


@api_view(['GET'])
def GetInvestigationData(request, investigationId):
    investigationDetails = Investigation.objects.get(id=investigationId)
    investigationDetails_Serializer = InvestigationSerializer(
        investigationDetails, many=False)

    outgoing = GetInvestigationDataSubFunc_ob_count(0, investigationId)
    incoming = GetInvestigationDataSubFunc_ob_count(1, investigationId)

    return Response({
        "investigation": investigationDetails_Serializer.data,
        "trackingNo": "077777777",
        "imei": "11111",
        "imsi": "00000",
        "outgoing": outgoing,
        "incoming": incoming
    })


@api_view(['GET'])
def GetInvestigation_AdditionalDetails(request, call_type, investigationId):
    attempts = GetInvestigationDataSubFunc_ob_count(call_type, investigationId)
    duration = GetInvestigationDataSubFunc_ob_duration(
        call_type, investigationId)
    date_time = GetInvestigationDataSubFunc_ob_date(call_type, investigationId)

    return Response({
        "attempts": attempts,
        "duration": duration,
        "date_time": date_time
    })


def GetInvestigationDataSubFunc_ob_count(call_type, investigation_id):
    investigationData = InvestigationData.objects.filter(call_type=call_type, investigation_id=investigation_id).values(
        'receiver').annotate(count=Count('receiver')).annotate(duration=Sum('duration')).order_by('-count')
    return investigationData


def GetInvestigationDataSubFunc_ob_duration(call_type, investigation_id):
    investigationData = InvestigationData.objects.filter(call_type=call_type, investigation_id=investigation_id).values(
        'receiver').annotate(count=Count('receiver')).annotate(duration=Sum('duration')).order_by('-duration')
    return investigationData


def GetInvestigationDataSubFunc_ob_date(call_type, investigation_id):
    investigationData = InvestigationData.objects.filter(
        call_type=call_type, investigation_id=investigation_id).order_by('created_at').reverse()
    serializer = InvestigationDataSerializer(investigationData, many=True)
    return serializer.data
