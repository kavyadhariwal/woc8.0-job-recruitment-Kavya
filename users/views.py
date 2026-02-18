from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from jobs.models import Job
from django.contrib import messages

def home(request):
    roles = ['Job Seeker', 'Employer', 'Admin']
    jobs = Job.objects.all().order_by('-date_posted')[:6]


    return render(request, 'home.html', {
        'roles': roles,
        'jobs': jobs
    })


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()   
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        if user.user_type == 'job_seeker':
            return '/dashboard/' 
        elif user.user_type == 'employer':
            return '/dashboard/'   
        return '/'


@login_required
def dashboard(request):
    profile = request.user.userprofile
    return render(request, 'dashboard.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html')

