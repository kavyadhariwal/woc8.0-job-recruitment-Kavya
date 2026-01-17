from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    roles = ['Job Seeker', 'Employer', 'Admin']
    return render(request, 'home.html', {'roles': roles})
