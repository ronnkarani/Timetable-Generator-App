from django.shortcuts import render
from .models import Stream, StreamSubjectTeacher, TimeSlot, Subject, Teacher, SchoolClass
import random
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.db.models import Count
from datetime import time


def generate_timetables(request):
    streams = Stream.objects.all()
    timeslots = list(TimeSlot.objects.all().order_by('day', 'start_time'))
    timetable_data = {}
    teacher_schedule = {}

    # Define standard break times (you can adjust as needed)
    breaks = {
        time(9, 20): "SHORT BREAK",
        time(10, 50): "LONG BREAK",
        time(12, 40): "LUNCH BREAK",
    }

    for stream in streams:
        timetable_data[stream] = {}
        assignments = list(StreamSubjectTeacher.objects.filter(stream=stream))
        if not assignments:
            continue

        random.shuffle(assignments)
        random.shuffle(timeslots)

        for slot in timeslots:
            day = slot.day
            if day not in timetable_data[stream]:
                timetable_data[stream][day] = {}

            # Check if this slot is a break
            if slot.start_time in breaks:
                timetable_data[stream][day][slot.start_time] = {
                    'subject': breaks[slot.start_time],
                    'teacher': '',
                    'is_break': True
                }
                continue

            if not assignments:
                continue

            subject_teacher = assignments.pop(0)
            key = (slot.day, slot.start_time, subject_teacher.teacher.id)
            if key in teacher_schedule:
                continue

            teacher_schedule[key] = True
            timetable_data[stream][day][slot.start_time] = {
                'subject': subject_teacher.subject.name,
                'teacher': subject_teacher.teacher.name,
                'is_break': False
            }

    return render(request, 'generated.html', {'timetable_data': timetable_data})

def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="timetable.pdf"'
    p = canvas.Canvas(response, pagesize=A4)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, "Generated School Timetable")

    y = 770
    from .models import Stream, StreamSubjectTeacher
    for stream in Stream.objects.all():
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, f"{stream}")
        y -= 20
        for stt in StreamSubjectTeacher.objects.filter(stream=stream)[:5]:
            p.setFont("Helvetica", 12)
            p.drawString(60, y, f"{stt.subject.name} - {stt.teacher.name}")
            y -= 15
        y -= 20

    p.showPage()
    p.save()
    return response


def admin_summary(request):
    context = {
        'teachers': Teacher.objects.count(),
        'classes': SchoolClass.objects.count(),
        'streams': Stream.objects.count(),
        'subjects': Subject.objects.count(),
        'assignments': StreamSubjectTeacher.objects.count(),
    }
    return render(request, 'summary.html', context)