from django.db import models
from accounts.models import School

# ===== HOW IT WORKS =====
class HowItWorksStep(models.Model):
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="FontAwesome icon class")

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number} - {self.title}"


# ===== SERVICES =====
class ServicePlan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('max', 'Max'),
    ]
    name = models.CharField(max_length=50, choices=PLAN_CHOICES)
    price = models.CharField(max_length=50)
    features = models.TextField(help_text="Comma-separated list of features")

    def feature_list(self):
        return self.features.split(',')

    def __str__(self):
        return self.name


# ===== FAQ =====
class FAQCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class FAQItem(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question


# ===== TESTIMONIALS =====
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='testimonials/')
    text = models.TextField()

    def __str__(self):
        return self.name

class Timetable(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.school.name}"
class SchoolClass(models.Model):
    """E.g. Class 1, Class 2, ..."""
    school = models.ForeignKey('accounts.School', on_delete=models.CASCADE, related_name='classes',default=1)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Stream(models.Model):
    """Each class can have multiple streams (e.g., 7A, 7B)"""
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=10)  # e.g., "A"

    def __str__(self):
        return f"{self.school_class.name}{self.name}"


class Subject(models.Model):
    """Subjects in the school."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Teacher info."""
    name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class StreamSubjectTeacher(models.Model):
    """Link between stream, subject, and teacher."""
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stream} - {self.subject} ({self.teacher})"


class TimeSlot(models.Model):
    """Defines one slot in the daily timetable (lesson or break)."""
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"
