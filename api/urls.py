from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),
    path('user/', views.UserRecordView.as_view(), name='users'),
    path('get_investigations', views.GetAllInvestigations,
         name='investigation.all'),
    path('get_investigation/<int:pk>',
         views.GetInvestigation, name='investigation.single'),
    path('create_investigation',
         views.CreateInvestigation, name='investigation.create'),
    path('delete_investigation/<int:investigationId>',
         views.DeleteInvestigation, name='investigation.delete'),


    path('get_investigation_data/<int:investigationId>',
         views.GetInvestigationData, name='investigationData.all'),
    path('get_investigation_additional/<int:call_type>/<int:investigationId>',
         views.GetInvestigation_AdditionalDetails, name='investigationData.all'),
]
