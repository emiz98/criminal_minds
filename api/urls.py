from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),
    path('get_investigations', views.GetAllInvestigations,
         name='investigation.all'),
    path('get_investigation/<int:pk>',
         views.GetInvestigation, name='investigation.single'),
    path('create_investigation',
         views.CreateInvestigation, name='investigation.create'),

    path('get_investigation_data/<int:investigationId>',
         views.GetInvestigationData, name='investigationData.all'),
    path('get_investigation_data_by_call_type/<int:call_type>',
         views.GetInvestigationDataByCallType, name='investigationData.all'),
]
