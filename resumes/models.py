from django.db import models
from django.contrib.auth.models import User

TEMPLATE_CHOICES = [
    ('modern', 'Modern'),
    ('classic', 'Classic'),
    ('creative', 'Creative'),
]

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, default='My Resume')
    full_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    projects = models.TextField(
        blank=True,
        help_text="Describe projects, technologies used, and outcomes"
    )
    certifications = models.TextField(
        blank=True,
        help_text="List certifications with issuing organization"
    )
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='modern')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
