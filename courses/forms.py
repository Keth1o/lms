from django import forms
from .models import Course, Subject, Schedule, Assignment

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['title', 'description']


class StudentRegistrationForm(forms.Form):

    username = forms.CharField(label="Логін")
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Пароль"
    )


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ['name', 'description', 'courses']


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ['title', 'date', 'description']


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'image', 'deadline']