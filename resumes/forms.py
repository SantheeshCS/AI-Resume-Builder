from django import forms
from .models import Resume
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title',
            'full_name',
            'email',
            'phone',
            'location',
            'job_title',
            'summary',
            'skills',
            'experience',
            'education',
            "projects",
            "certifications",
            'template',
        ]

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
