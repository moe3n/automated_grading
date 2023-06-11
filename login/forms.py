from django import forms
from database.models import user, subject, exams, question_set, question


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ('username', 'password', 'role')


class SubjectForm(forms.ModelForm):
    class Meta:
        model = subject
        fields = ['subject_name']


class ExamForm(forms.ModelForm):
    class Meta:
        model = exams
        fields = ['exam_name']


class SetForm(forms.ModelForm):
    class Meta:
        model = question_set
        fields = ['set_number']
