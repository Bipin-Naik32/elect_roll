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
]
