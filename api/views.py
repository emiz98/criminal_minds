from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Sum
from datetime import datetime

from api.data_extraction import data_pipeline3, data_pipeline, data_pipeline2, data_pipeline4, date_convert
from .serializers import InvestigationDataSerializer, InvestigationSerializer, UserSerializer
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


class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


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
    serializer = InvestigationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    # investigation = GetInvestigationSub(serializer.data['id'])
    # if int(request.data['network']) == 0:
    #     df = data_pipeline4(pdf)
    #     for index, row in df.iterrows():
    #         data_row = InvestigationData(
    #             investigation=investigation,
    #             caller=row["caller"],
    #             receiver=row["receiver"], call_type=row["call_type"],
    #             duration=row["duration"], imei=row["imei"], imsi=row["imei"], created_at=datetime.strptime(
    #                 row["date_time"], '%m/%d/%Y %H:%M:%S')
    #         )
    #         data_row.save()
    # elif int(request.data['network']) == 1:
    #     df = data_pipeline2(pdf)
    #     for index, row in df.iterrows():
    #         data_row = InvestigationData(
    #             investigation=investigation,
    #             caller=row["caller"],
    #             receiver=row["receiver"], call_type=row["call_type"],
    #             duration=row["duration"], imei=row["imei"], imsi=row["imei"], created_at=datetime.strptime(
    #                 date_convert(row["date_time"]), '%m/%d/%Y %H:%M:%S')
    #         )
    #         data_row.save()
    # elif int(request.data['network']) == 2:
    #     df = data_pipeline3(pdf)
    #     for index, row in df.iterrows():
    #         data_row = InvestigationData(
    #             investigation=investigation,
    #             caller=row["caller"],
    #             receiver=row["receiver"], call_type=row["call_type"],
    #             duration=row["duration"], imei=row["imei"], imsi=row["imei"], created_at=datetime.strptime(
    #                 row["date_time"], '%m/%d/%Y %H:%M:%S')
    #         )
    #         data_row.save()
    # elif int(request.data['network']) == 3:
        # df = data_pipeline(pdf)
        # for index, row in df.iterrows():
        #     data_row = InvestigationData(
        #         investigation=investigation,
        #         caller=row["caller"],
        #         receiver=row["receiver"], call_type=row["call_type"],
        #         duration=0 if row["duration"] else row["duration"], imei=row["imei"], imsi=row["imei"], created_at=datetime.strptime(
        #             row["date_time"], '%m/%d/%Y %H:%M:%S')
        #     )
        #     data_row.save()

    return Response(serializer.data)


@api_view(['GET'])
def DeleteInvestigation(request, investigationId):
    investigation = Investigation.objects.get(id=investigationId)
    investigationData = InvestigationData.objects.filter(
        investigation_id=investigationId)
    for i in range(len(investigationData)):
        investigationData[i].delete()
    investigation.delete()
    return Response("Investigation deleted successfully")


@api_view(['GET'])
def GetInvestigationData(request, investigationId):
    investigationDetails = Investigation.objects.get(id=investigationId)
    investigationDetails_Serializer = InvestigationSerializer(
        investigationDetails, many=False)

    singleData = InvestigationData.objects.filter(
        investigation_id=investigationId).first()
    serializer = InvestigationDataSerializer(singleData, many=False)

    outgoing = GetInvestigationDataSubFunc_ob_count(0, investigationId)
    incoming = GetInvestigationDataSubFunc_ob_count(1, investigationId)

    return Response({
        "investigation": investigationDetails_Serializer.data,
        "trackingNo": serializer.data['caller'],
        "imei": serializer.data['imei'],
        "imsi": serializer.data['imsi'],
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


def GetInvestigationSub(invID):
    investigation = Investigation.objects.get(id=invID)
    return investigation
