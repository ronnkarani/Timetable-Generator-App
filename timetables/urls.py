from django.urls import path
from . import views


urlpatterns = [
    # Pages
    path('', views.home, name='home'), 
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact, name='contact'),

    # Dashboard / Home
    path('dashboard/', views.dashboard, name='dashboard'),

    # Teacher management
    path('teachers/', views.list_teachers, name='teachers'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/<int:teacher_id>/', views.view_teacher, name='view_teacher'),
    path('teachers/<int:teacher_id>/edit/', views.edit_teacher, name='edit_teacher'),
    path('teachers/<int:teacher_id>/delete/', views.delete_teacher, name='delete_teacher'),

    # Class management
    path('classes/', views.list_classes, name='classes'),
    path('classes/add/', views.add_class, name='add_class'),
    path('classes/<int:class_id>/', views.view_class, name='view_class'),
    path('classes/<int:class_id>/edit/', views.edit_class, name='edit_class'),
    path('classes/<int:class_id>/delete/', views.delete_class, name='delete_class'),

    # Subject management
    path('subjects/add/', views.add_subject, name='add_subject'),

    # Stream-Subject-Teacher Assignments
    path('assignments/', views.list_assignments, name='assignments'),
    path('assignments/add/', views.add_stream_subject_teacher, name='add_assignment'),
    path('assignments/<int:assignment_id>/', views.view_assignment, name='view_assignment'),
    path('assignments/<int:assignment_id>/edit/', views.edit_assignment, name='edit_assignment'),
    path('assignments/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),

    # Timetable generation
    path('generate/', views.generate_timetables, name='generate_timetables'),
]