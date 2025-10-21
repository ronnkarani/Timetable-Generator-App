from django import forms
from django.forms import inlineformset_factory
from .models import Teacher, SchoolClass, Subject, TimeSlot, Stream, StreamSubjectTeacher

class StreamSubjectTeacherForm(forms.ModelForm):
    class Meta:
        model = StreamSubjectTeacher
        fields = ['stream', 'subject', 'teacher']

    # Optional: customize labels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stream'].queryset = Stream.objects.all()
        self.fields['subject'].queryset = Subject.objects.all()
        self.fields['teacher'].queryset = Teacher.objects.all()

class StreamForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['name', 'school_class'] 

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'teacher_id']

class ClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ['name']
        
# Inline formset: Stream forms linked to SchoolClass
StreamFormSet = inlineformset_factory(
    SchoolClass,
    Stream,
    fields=['name'],
    extra=2,  # Number of empty streams to show by default
    can_delete=True
)

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['name', 'start_time', 'end_time', 'is_break']
