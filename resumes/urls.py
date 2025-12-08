from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    
    path("resume/new/", views.resume_new_view, name="resume_new"),
    path("resume/<int:resume_id>/edit/", views.resume_editor_view, name="editor"),


    path('resume/<int:resume_id>/autosave/', views.autosave_view, name='autosave'),

    path('resume/<int:resume_id>/ai/summary/', views.ai_summary_view, name='ai_summary'),
    path('resume/<int:resume_id>/ai/experience/', views.ai_experience_view, name='ai_experience'),
    path('resume/<int:resume_id>/ai/keywords/', views.ai_keywords_view, name='ai_keywords'),

    path(
    "resume/<int:resume_id>/pdf/",
    views.resume_pdf_preview,
    name="resume_pdf",
),


    path(
    'resume/<int:resume_id>/delete/',
    views.delete_resume_view,
    name='resume_delete'),
    
    path(
    'resumes/delete-all/',
    views.delete_all_resumes_view,
    name='resumes_delete_all'
),
]
