import os
import django
from datetime import datetime, time, timedelta

import random

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "timetable_system.settings")
django.setup()

from timetables.models import SchoolClass, Stream, Subject, Teacher, StreamSubjectTeacher, TimeSlot

print("🧹 Clearing old data...")
StreamSubjectTeacher.objects.all().delete()
TimeSlot.objects.all().delete()
Stream.objects.all().delete()
SchoolClass.objects.all().delete()
Subject.objects.all().delete()
Teacher.objects.all().delete()
print("✅ Previous data cleared!")

# 1️⃣ Grades & Streams
grades = []
for i in range(1, 9):
    grade = SchoolClass.objects.create(name=f"Grade {i}")
    for stream_letter in ["A", "B", "C"]:
        Stream.objects.create(school_class=grade, name=stream_letter)
    grades.append(grade)
print("✅ Added Grades 1–8 with streams A, B, C")

# 2️⃣ Subjects
subject_names = [
    "Mathematics", "English", "Kiswahili", "Science",
    "Social Studies", "CRE", "Music", "Art", "PE"
]
subjects = [Subject.objects.create(name=name) for name in subject_names]
print("✅ Added subjects")

# 3️⃣ Teachers
teacher_names = [
    "Alice Mwangi", "Brian Otieno", "Carol Njeri", "David Kamau",
    "Eva Wambui", "Frank Oduor", "Grace Mutua", "Henry Maina",
    "Irene Chebet", "James Karanja", "Lucy Wanjiku", "Mark Njenga",
    "Nancy Maina", "Oscar Mworia", "Patricia Kimani", "Quincy Njoroge",
    "Rachel Wairimu", "Samuel Kibet", "Theresa Nyambura", "Victor Ochieng"
]
teachers = [Teacher.objects.create(name=name, teacher_id=f"T{idx+1:03d}")
            for idx, name in enumerate(teacher_names)]
print("✅ Added 20 teachers")

# 4️⃣ Assign subjects to streams
streams = Stream.objects.all()
for stream in streams:
    shuffled_subjects = subjects.copy()
    random.shuffle(shuffled_subjects)
    for subject in shuffled_subjects:
        teacher = random.choice(teachers)
        StreamSubjectTeacher.objects.create(stream=stream, subject=subject, teacher=teacher)
print("✅ Assigned subjects to all streams with teachers")

# 5️⃣ Create time slots (40 min classes + breaks)
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Class duration
class_duration = timedelta(minutes=40)

# Breaks with durations
breaks = [
    ("SHORT BREAK", timedelta(minutes=10)),
    ("LONG BREAK", timedelta(minutes=30)),
    ("LUNCH BREAK", timedelta(minutes=50)),
]

print("⏰ Creating time slots...")
for day in WEEK_DAYS:
    # Start at 8:00
    current_time = time(8, 0)
    current_datetime = datetime.combine(datetime.today(), current_time)

    # We'll generate slots until 16:00
    end_of_day = datetime.combine(datetime.today(), time(16, 0))

    break_index = 0  # cycle through breaks
    while current_datetime.time() < end_of_day.time():
        # Decide if we need a break now (example: Short break after 1 class, etc.)
        if break_index < len(breaks):
            break_name, break_duration = breaks[break_index]
            # Let's assume first break at 9:20, second at 11:20, third at 12:40
            if ((break_index == 0 and current_datetime.time() >= time(9,20)) or
                (break_index == 1 and current_datetime.time() >= time(11,20)) or
                (break_index == 2 and current_datetime.time() >= time(12,40))):
                end_time = (current_datetime + break_duration).time()
                TimeSlot.objects.create(day=day, start_time=current_datetime.time(),
                                        end_time=end_time, is_break=True, break_name=break_name)
                current_datetime += break_duration
                break_index += 1
                continue

        # Regular class
        end_time = (current_datetime + class_duration).time()
        if end_time > time(16,0):
            break
        TimeSlot.objects.create(day=day, start_time=current_datetime.time(), end_time=end_time)
        current_datetime += class_duration

print("✅ Time slots and breaks created successfully!")
print("🎉 Data population complete!")
