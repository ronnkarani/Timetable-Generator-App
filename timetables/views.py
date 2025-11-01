from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import time
from .models import Stream, StreamSubjectTeacher, Subject, Teacher, SchoolClass, TimeSlot, Timetable
from .forms import TeacherForm, ClassForm, SubjectForm, StreamSubjectTeacherForm, StreamFormSet
from datetime import datetime, timedelta
from django.db.models import Q
import random
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from accounts.models import User, School

# Root   Redirect
def root_redirect(request):
    """Show Home page as default landing page for all users."""
    return render(request, 'pages/home.html')


def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def faqs(request):
    return render(request, 'pages/faqs.html')

def contact(request):
    return render(request, 'pages/contact.html')


# Dashboard page
@login_required
def dashboard(request):
    user = request.user

    context = {}

    if user.is_superuser or user.role == 'superadmin':
        # Show all schools and their admins
        schools = School.objects.all()
        school_admins = User.objects.filter(role='admin')
        timetables = Timetable.objects.all()
        context.update({
            'is_superadmin': True,
            'schools': schools,
            'school_admins': school_admins,
            'timetables': timetables,
        })
    elif user.role == 'admin':
        # Show the current school data
        school = user.school
        teachers = Teacher.objects.filter(
            streamsubjectteacher__stream__school_class__school=school
        ).distinct()
        subjects = Subject.objects.all()
        classes = SchoolClass.objects.all()
        streams = Stream.objects.all()
        assignments = StreamSubjectTeacher.objects.all()
        timetables = Timetable.objects.filter(school=school)
        context.update({
            'is_admin': True,
            'school': school,
            'teachers': teachers,
            'subjects': subjects,
            'classes': classes,
            'streams': streams,
            'assignments': assignments,
            'timetables': timetables,
        })
    else:
        # Not logged in or placeholder
        context.update({
            'is_guest': True,
        })

    return render(request, 'dashboard.html', context)


# Add Teacher
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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

@login_required
def view_class(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)
    streams = school_class.streams.all()  # all streams
    # Build a dict for subjects/teachers per stream
    stream_assignments = {}
    for stream in streams:
        assignments = StreamSubjectTeacher.objects.filter(stream=stream)
        stream_assignments[stream] = assignments

    return render(request, 'view_detail.html', {
        'object': school_class,
        'type': 'class',
        'title': f'Class: {school_class.name}',
        'return_url': 'classes',
        'edit_url': 'edit_class',
        'delete_url': 'delete_class',
        'stream_assignments': stream_assignments
    })


@login_required
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
@login_required
def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    TeacherAssignmentFormSet = modelformset_factory(
        StreamSubjectTeacher,
        form=StreamSubjectTeacherForm,
        extra=1,
        can_delete=True
    )
    queryset = StreamSubjectTeacher.objects.filter(teacher=teacher)
    formset = TeacherAssignmentFormSet(request.POST or None, queryset=queryset)

    teacher_form = TeacherForm(request.POST or None, instance=teacher)

    if teacher_form.is_valid() and formset.is_valid():
        teacher_form.save()
        instances = formset.save(commit=False)
        for inst in instances:
            inst.teacher = teacher
            inst.save()
        # Delete any removed items
        for inst in formset.deleted_objects:
            inst.delete()
        return redirect('teachers')

    return render(request, 'add_form.html', {
        'form': teacher_form,
        'formset': formset,
        'title': 'Edit Teacher',
        'form_type': 'teacher'
    })

# Delete Teacher
@login_required
def delete_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teachers')
    return render(request, 'confirm_delete.html', {'object': teacher, 'type': 'Teacher'})


# Edit Class
@login_required
def edit_class(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)

    # ----------------- MAIN CLASS FORM -----------------
    class_form = ClassForm(request.POST or None, instance=school_class)

    # ----------------- STREAMS FORMSET -----------------
    StreamFormSetForClass = modelformset_factory(
        Stream,
        form=StreamFormSet.form,  # use the same form as add_class
        extra=1,
        can_delete=True
    )
    stream_queryset = Stream.objects.filter(school_class=school_class)
    stream_formset = StreamFormSetForClass(request.POST or None, queryset=stream_queryset)

    # ----------------- SUBJECT-TEACHER ASSIGNMENT FORMSETS PER STREAM -----------------
    StreamSubjectTeacherFormSet = modelformset_factory(
        StreamSubjectTeacher,
        form=StreamSubjectTeacherForm,
        extra=1,
        can_delete=True
    )

    stream_assignment_formsets = []
    for stream in stream_queryset:
        qs = StreamSubjectTeacher.objects.filter(stream=stream)
        # ⚡ IMPORTANT: Add a unique prefix for each stream to avoid conflicts
        fs = StreamSubjectTeacherFormSet(request.POST or None, queryset=qs, prefix=f'stream_{stream.id}')
        stream_assignment_formsets.append((stream, fs))  # store tuple (stream, formset)

    # ----------------- FORM VALIDATION -----------------
    # Check all forms before saving
    if class_form.is_valid() and stream_formset.is_valid() and all(fs.is_valid() for _, fs in stream_assignment_formsets):
        # Save class
        class_form.save()

        # Save streams
        stream_instances = stream_formset.save(commit=False)
        for inst in stream_instances:
            inst.school_class = school_class
            inst.save()
        # Delete removed streams
        for inst in stream_formset.deleted_objects:
            inst.delete()

        # Save stream-subject-teacher assignments
        for stream, fs in stream_assignment_formsets:
            instances = fs.save(commit=False)
            for inst in instances:
                inst.stream = stream  # assign the correct stream
                inst.save()
            for inst in fs.deleted_objects:
                inst.delete()

        return redirect('classes')

    return render(request, 'add_form.html', {
        'form': class_form,
        'formset': stream_formset,
        'stream_assignment_formsets': stream_assignment_formsets,
        'title': f'Edit Class: {school_class.name}',
        'form_type': 'class',
        'school_class': school_class  # pass the class for reference
    })

# Delete Class
@login_required
def delete_class(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)
    if request.method == 'POST':
        school_class.delete()
        return redirect('classes')
    return render(request, 'confirm_delete.html', {'object': school_class, 'type': 'Class'})


# Edit Assignment
@login_required
def edit_assignment(request, assignment_id):
    assignment = StreamSubjectTeacher.objects.get(id=assignment_id)
    form = StreamSubjectTeacherForm(request.POST or None, instance=assignment)
    if form.is_valid():
        form.save()
        return redirect('assignments')
    return render(request, 'add_form.html', {'form': form, 'title': 'Edit Assignment'})

# Delete Assignment
@login_required
def delete_assignment(request, assignment_id):
    assignment = StreamSubjectTeacher.objects.get(id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments')
    return render(request, 'confirm_delete.html', {'object': assignment, 'type': 'Assignment'})


# List Teachers
@login_required
def list_teachers(request):
    query = request.GET.get('q', '')
    teachers = Teacher.objects.filter(name__icontains=query) if query else Teacher.objects.all()
    
    paginator = Paginator(teachers, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list_teachers.html', {'teachers': page_obj, 'query': query, 'page_obj': page_obj})


# List Classes
@login_required
def list_classes(request):
    classes = SchoolClass.objects.all()
    page_number = request.GET.get('page')

    # Build a structure: class -> streams -> subjects & teachers
    class_data = []
    for cls in classes:
        streams_data = []
        for stream in cls.streams.all():
            assignments = StreamSubjectTeacher.objects.filter(stream=stream)
            streams_data.append({
                'stream': stream,
                'assignments': assignments
            })
        class_data.append({
            'class': cls,
            'streams_data': streams_data
        })

    # Pagination
    paginator = Paginator(class_data, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_classes.html', {
        'class_data': page_obj,
        'page_obj': page_obj
    })


# List Assignments
@login_required
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
@login_required
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




