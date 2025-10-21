from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import time
from .models import Stream, StreamSubjectTeacher, TimeSlot, Subject, Teacher, SchoolClass
from .forms import TeacherForm, ClassForm, SubjectForm, TimeSlotForm, StreamSubjectTeacherForm, StreamForm, StreamFormSet
from datetime import datetime, timedelta
from django.db.models import Q
import random


# Dashboard page
def dashboard(request):
    return render(request, 'dashboard.html')


def add_teacher(request):
    form = TeacherForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('teachers')
    return render(request, 'add_form.html', {'form': form, 'title': 'Add Teacher'})

def add_class(request):
    if request.method == 'POST':
        class_form = ClassForm(request.POST)
        formset = StreamFormSet(request.POST)

        if class_form.is_valid() and formset.is_valid():
            new_class = class_form.save()
            streams = formset.save(commit=False)
            for stream in streams:
                stream.school_class = new_class
                stream.save()
            return redirect('classes')
    else:
        class_form = ClassForm()
        formset = StreamFormSet()

    return render(request, 'add_form.html', {
        'form': class_form,     # main form
        'formset': formset,     # inline streams
        'title': 'Add Class with Streams'
    })

def add_subject(request):
    form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('classes')
    return render(request, 'add_form.html', {'form': form, 'title': 'Add Subject'})

def add_timeslot(request):
    form = TimeSlotForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('timetables')
    return render(request, 'add_form.html', {'form': form, 'title': 'Add Timeslot'})

def add_stream_subject_teacher(request):
    from .forms import StreamSubjectTeacherForm
    form = StreamSubjectTeacherForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')  # or a list page if you want
    return render(request, 'add_form.html', {'form': form, 'title': 'Add Stream Subject Teacher'})

def add_stream(request):
    form = StreamForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')  # or list page if you have one
    return render(request, 'add_form.html', {'form': form, 'title': 'Add Stream'})

# List Teachers
def list_teachers(request):
    query = request.GET.get('q', '')
    if query:
        teachers = Teacher.objects.filter(name__icontains=query)
    else:
        teachers = Teacher.objects.all()
    return render(request, 'list_teachers.html', {'teachers': teachers, 'query': query})



# List Classes
def list_classes(request):
    classes = SchoolClass.objects.all()
    return render(request, 'list_classes.html', {'classes': classes})

def list_assignments(request):
    query = request.GET.get('q', '')
    assignments = StreamSubjectTeacher.objects.select_related('stream', 'subject', 'teacher')
    if query:
        assignments = assignments.filter(
            Q(stream__name__icontains=query) |
            Q(subject__name__icontains=query) |
            Q(teacher__name__icontains=query)
        )
    return render(request, 'list_assignments.html', {'assignments': assignments, 'query': query})




def generate_timetables(request):
    regenerate = request.GET.get('regenerate', '0') == '1'

    if regenerate:
        # Clear old timeslots to force regeneration
        TimeSlot.objects.all().delete()
    streams = Stream.objects.all()
    timeslots = list(TimeSlot.objects.all().order_by('start_time'))
    timetable_data = {}
    WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # ✅ If no timeslots exist, auto-generate the full-day schedule
    if not timeslots:
        lesson_duration = timedelta(minutes=40)
        short_break = timedelta(minutes=10)
        long_break = timedelta(minutes=30)
        lunch_break = timedelta(minutes=80)

        start_time = datetime.combine(datetime.today(), time(8, 0))
        current_time = start_time
        lesson_count = 0

        # Generate 9 lessons total (3 after each break)
        while lesson_count < 9:
            # Add a lesson
            lesson_end = current_time + lesson_duration
            TimeSlot.objects.create(
                name=f"Lesson {lesson_count + 1}",
                start_time=current_time.time(),
                end_time=lesson_end.time(),
                is_break=False
            )
            lesson_count += 1
            current_time = lesson_end

            # Insert breaks in correct order
            if lesson_count == 2:
                # Short Break
                TimeSlot.objects.create(
                    name="Short Break",
                    start_time=current_time.time(),
                    end_time=(current_time + short_break).time(),
                    is_break=True
                )
                current_time += short_break

            elif lesson_count == 4:
                # Long Break
                TimeSlot.objects.create(
                    name="Long Break",
                    start_time=current_time.time(),
                    end_time=(current_time + long_break).time(),
                    is_break=True
                )
                current_time += long_break

            elif lesson_count == 6:
                # Lunch Break
                TimeSlot.objects.create(
                    name="Lunch Break",
                    start_time=current_time.time(),
                    end_time=(current_time + lunch_break).time(),
                    is_break=True
                )
                current_time += lunch_break

        # Reload timeslots from DB
        timeslots = list(TimeSlot.objects.all().order_by('start_time'))

    # ✅ Assign subjects and teachers
    for stream in streams:
        timetable_data[str(stream)] = {}
        assignments = list(StreamSubjectTeacher.objects.filter(stream=stream))
        if not assignments:
            continue

        # Shuffle assignments to create a new timetable each time
        random.shuffle(assignments)

        teacher_schedule = {}
        subject_index = 0

        for day in WEEK_DAYS:
            timetable_data[str(stream)][day] = {}
            for slot in timeslots:
                slot_label = f"{slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}"
                if slot.is_break:
                    timetable_data[str(stream)][day][slot_label] = {
                        'subject': slot.name,
                        'teacher': '',
                        'is_break': True
                    }
                    continue

                # Assign subject/teacher
                subject_teacher = assignments[subject_index % len(assignments)]
                key = (day, slot.start_time, subject_teacher.teacher.id)
                attempts = 0
                while key in teacher_schedule and attempts < len(assignments):
                    subject_index += 1
                    subject_teacher = assignments[subject_index % len(assignments)]
                    key = (day, slot.start_time, subject_teacher.teacher.id)
                    attempts += 1

                teacher_schedule[key] = True
                timetable_data[str(stream)][day][slot_label] = {
                    'subject': subject_teacher.subject.name,
                    'teacher': subject_teacher.teacher.name,
                    'is_break': False
                }
                subject_index += 1

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

