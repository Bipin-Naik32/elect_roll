from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-record/', views.add_record, name='add_record'),
    path('search-records/', views.search_records, name='search_records'),
    path('send-sms/', views.send_sms, name='send_sms'),
    path('return-to-dashboard/', views.return_to_dashboard, name='return_to_dashboard'),
    path('suggest-voter-id/', views.suggest_voter_id, name='suggest_voter_id'),
    path('edit-record/<int:record_id>/', views.edit_record, name='edit_record'),
    path('export-vcf/', views.export_vcf, name='export_vcf'), 
    path('gradation/',views.gradation_home,name='gradation_home'),
    path('gradation/list/',views.gradation_list,name='gradation_list'),
    path('gradation/edit/<int:voter_id>/',views.gradation_edit,name='gradation_edit'),
    path('gradation/get-castes/',views.get_castes, name='get_castes'),  
]
