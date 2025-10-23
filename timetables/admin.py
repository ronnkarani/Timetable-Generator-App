from django.contrib import admin
from .models import SchoolClass, Stream, Subject, Teacher, StreamSubjectTeacher

admin.site.register(SchoolClass)
admin.site.register(Stream)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(StreamSubjectTeacher)
