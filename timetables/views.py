from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import time
from .models import Stream, StreamSubjectTeacher, Subject, Teacher, SchoolClass
from .forms import TeacherForm, ClassForm, SubjectForm, StreamSubjectTeacherForm, StreamFormSet
from datetime import datetime, timedelta
from django.db.models import Q
import random
from django.core.paginator import Paginator


# Dashboard page
def dashboard(request):
    return render(request, 'dashboard.html')


# Add Teacher
def add_teacher(request):
    form = TeacherForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('teachers')
    return render(request, 'add_form.html', {
        'form': form, 
        'title': 'Add Teacher',
        'form_type': 'teacher'
        })


# Add Class with inline Streams
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
        'title': 'Add Class with Streams',
        'form_type': 'class'
    })


# Add Subject   
def add_subject(request):
    form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('classes')
    return render(request, 'add_form.html', {
        'form': form, 
        'title': 'Add Subject',
        'form_type': 'subject'
    })


# Add Stream Subject Teacher Assignment
def add_stream_subject_teacher(request):
    from .forms import StreamSubjectTeacherForm
    form = StreamSubjectTeacherForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')  # or a list page if you want
    return render(request, 'add_form.html', {
        'form': form, 
        'title': 'Add Stream Subject Teacher',
        'form_type': 'assignment'
        })



# View details (universal)
def view_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    return render(request, 'view_detail.html', {
        'object': teacher,
        'type': 'teacher',
        'title': 'Teacher',
        'return_url': 'teachers',
        'edit_url': 'edit_teacher',
        'delete_url': 'delete_teacher',
    })


def view_class(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)
    return render(request, 'view_detail.html', {
        'object': school_class,
        'type': 'class',
        'title': 'Class',
        'return_url': 'classes',
        'edit_url': 'edit_class',
        'delete_url': 'delete_class',
    })


def view_assignment(request, assignment_id):
    assignment = StreamSubjectTeacher.objects.get(id=assignment_id)
    return render(request, 'view_detail.html', {
        'object': assignment,
        'type': 'assignment',
        'title': 'Assignment',
        'return_url': 'assignments',
        'edit_url': 'edit_assignment',
        'delete_url': 'delete_assignment',
    })

# Edit Teacher
def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    form = TeacherForm(request.POST or None, instance=teacher)
    if form.is_valid():
        form.save()
        return redirect('teachers')
    return render(request, 'add_form.html', {'form': form, 'title': 'Edit Teacher'})

# Delete Teacher
def delete_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teachers')
    return render(request, 'confirm_delete.html', {'object': teacher, 'type': 'Teacher'})


# Edit Class
def edit_class(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)
    form = ClassForm(request.POST or None, instance=school_class)
    if form.is_valid():
        form.save()
        return redirect('classes')
    return render(request, 'add_form.html', {'form': form, 'title': 'Edit Class'})

# Delete Class
def delete_class(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)
    if request.method == 'POST':
        school_class.delete()
        return redirect('classes')
    return render(request, 'confirm_delete.html', {'object': school_class, 'type': 'Class'})


# Edit Assignment
def edit_assignment(request, assignment_id):
    assignment = StreamSubjectTeacher.objects.get(id=assignment_id)
    form = StreamSubjectTeacherForm(request.POST or None, instance=assignment)
    if form.is_valid():
        form.save()
        return redirect('assignments')
    return render(request, 'add_form.html', {'form': form, 'title': 'Edit Assignment'})

# Delete Assignment
def delete_assignment(request, assignment_id):
    assignment = StreamSubjectTeacher.objects.get(id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments')
    return render(request, 'confirm_delete.html', {'object': assignment, 'type': 'Assignment'})


# List Teachers
def list_teachers(request):
    query = request.GET.get('q', '')
    teachers = Teacher.objects.filter(name__icontains=query) if query else Teacher.objects.all()
    
    paginator = Paginator(teachers, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list_teachers.html', {'teachers': page_obj, 'query': query, 'page_obj': page_obj})


# List Classes
def list_classes(request):
    classes = SchoolClass.objects.all()
    paginator = Paginator(classes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list_classes.html', {'classes': page_obj, 'page_obj': page_obj})


# List Assignments
def list_assignments(request):
    query = request.GET.get('q', '')
    assignments = StreamSubjectTeacher.objects.select_related('stream', 'subject', 'teacher')
    if query:
        assignments = assignments.filter(
            Q(stream__name__icontains=query) |
            Q(subject__name__icontains=query) |
            Q(teacher__name__icontains=query)
        )
    paginator = Paginator(assignments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list_assignments.html', {'assignments': page_obj, 'query': query, 'page_obj': page_obj})
# Generate Timetables
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

    # Assign subjects and teachers
    for stream in streams:
        timetable_data[str(stream)] = {}
        assignments = list(StreamSubjectTeacher.objects.filter(stream=stream))
        if not assignments:
            continue

        # Shuffle assignments to create a new timetable each time for regenerating
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


#Download Timetable as PDF file
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

