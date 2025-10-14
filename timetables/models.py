from django.db import models

class SchoolClass(models.Model):
    """E.g. Class 1, Class 2, ..."""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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
    """Uniform time slots for all streams."""
    day = models.CharField(max_length=15)  # e.g. Monday
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day}: {self.start_time} - {self.end_time}"
