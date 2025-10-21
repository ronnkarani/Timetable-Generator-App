from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-class/', views.add_class, name='add_class'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('add-stream/', views.add_stream, name='add_stream'),
    path('add-timeslot/', views.add_timeslot, name='add_timeslot'),
    path('add-assignment/', views.add_stream_subject_teacher, name='add_assignment'),
    path('assignments/', views.list_assignments, name='assignments'),
    path('teachers/', views.list_teachers, name='teachers'),  # used in navbar
    path('classes/', views.list_classes, name='classes'),    # used in navbar
    path('timetables/', views.generate_timetables, name='generate_timetables'),
    path('timetables/download/', views.download_pdf, name='download_pdf'),
]
