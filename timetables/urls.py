from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-class/', views.add_class, name='add_class'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('add-assignment/', views.add_stream_subject_teacher, name='add_assignment'),
    
    # View details
path('teachers/<int:teacher_id>/', views.view_teacher, name='view_teacher'),
path('classes/<int:class_id>/', views.view_class, name='view_class'),
path('assignments/<int:assignment_id>/', views.view_assignment, name='view_assignment'),

    # Teachers
path('teachers/<int:teacher_id>/edit/', views.edit_teacher, name='edit_teacher'),
path('teachers/<int:teacher_id>/delete/', views.delete_teacher, name='delete_teacher'),

# Classes
path('classes/<int:class_id>/edit/', views.edit_class, name='edit_class'),
path('classes/<int:class_id>/delete/', views.delete_class, name='delete_class'),

# Assignments
path('assignments/<int:assignment_id>/edit/', views.edit_assignment, name='edit_assignment'),
path('assignments/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),

    
    path('assignments/', views.list_assignments, name='assignments'),
    path('teachers/', views.list_teachers, name='teachers'), 
    path('classes/', views.list_classes, name='classes'),   
    path('timetables/', views.generate_timetables, name='generate_timetables'),
    path('timetables/download/', views.download_pdf, name='download_pdf'),
]
