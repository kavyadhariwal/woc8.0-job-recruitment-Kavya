from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from jobs.models import Job
from django.contrib import messages
from .models import Application

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user
            application.save()
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply_job.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    applications = request.user.application_set.all()
    return render(request, 'applications/my_applications.html', {'applications': applications})

@login_required
def manage_applicants(request):
    applications = Application.objects.filter(job__employer=request.user)
    return render(request, 'applications/manage_applicants.html', {'applications': applications})


@login_required
def manage_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.employer:
        return redirect('job_list')

    applications = Application.objects.filter(job=job)

    return render(request, 'applications/manage_applications.html', {
        'job': job,
        'applications': applications
    })


@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id)

    if request.user != application.job.employer:
        return redirect('job_list')

    application.status = status
    application.save()

    messages.success(request, f"Application {status} successfully.")
    return redirect('manage_applications', job_id=application.job.id)

@login_required
def withdraw_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.user != application.applicant:
        return redirect('job_list')

    if application.status == "Pending":
        application.delete()
        messages.success(request, "Application withdrawn successfully.")

    return redirect('my_applications')
