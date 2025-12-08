from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .forms import ResumeForm, RegisterForm
from .models import Resume
from .ai import generate_summary, optimize_experience, suggest_keywords
from .pdf_utils import render_resume_pdf
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid credentials."
    return render(request, 'auth/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-updated')
    return render(request, 'dashboard.html', {'resumes': resumes})

@login_required
def resume_create_view(request):
    resume = Resume.objects.filter(user=request.user).order_by('-updated').first()

    if resume:
        return redirect('editor', resume_id=resume.id)

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('editor', resume_id=resume.id)
    else:
        form = ResumeForm()

    return render(request, 'editor.html', {'form': form, 'resume': None})

@login_required
def resume_editor_view(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
    else:
        form = ResumeForm(instance=resume)

    return render(
        request,
        "editor.html",
        {
            "form": form,
            "resume": resume
        }
    )


@login_required
def autosave_view(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        fields = ['title','full_name','email','phone','location','job_title','summary','skills','experience','education','template']
        for f in fields:
            if f in request.POST:
                setattr(resume, f, request.POST.get(f, ''))
        resume.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'}, status=400)

@login_required
def ai_summary_view(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        job = request.POST.get('job_title', resume.job_title)
        skills = request.POST.get('skills', resume.skills)
        years = request.POST.get('years', '1')
        text = generate_summary(job, skills, years)
        return JsonResponse({'summary': text})
    return JsonResponse({'error': 'Invalid'}, status=400)

@login_required
def ai_experience_view(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        exp = request.POST.get('experience', resume.experience)
        job = request.POST.get('job_title', resume.job_title)
        text = optimize_experience(exp, job)
        return JsonResponse({'experience': text})
    return JsonResponse({'error': 'Invalid'}, status=400)

@login_required
def ai_keywords_view(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        job = request.POST.get('job_title', resume.job_title)
        skills = request.POST.get('skills', resume.skills)
        text = suggest_keywords(job, skills)
        return JsonResponse({'keywords': text})
    return JsonResponse({'error': 'Invalid'}, status=400)

@login_required
def resume_pdf_preview(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return render(request, "resume_preview.html", {"resume": resume})

@login_required
@require_POST
def delete_resume_view(request, resume_id):
    resume = get_object_or_404(
        Resume, id=resume_id, user=request.user
    )
    resume.delete()
    return redirect('dashboard')

@login_required
@require_POST
def delete_all_resumes_view(request):
    Resume.objects.filter(user=request.user).delete()
    return redirect('dashboard')

@login_required
def resume_new_view(request):
    resume = Resume.objects.create(
        user=request.user,
        full_name="",
        job_title="",
        summary="",
        skills="",
        experience="",
        education="",
        template="modern"
    )
    return redirect("editor", resume_id=resume.id)
