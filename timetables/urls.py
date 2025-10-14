from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_timetables, name='generate_timetables'),
    path('download/', views.download_pdf, name='download_pdf'),
    path('summary/', views.admin_summary, name='admin_summary'),


]
