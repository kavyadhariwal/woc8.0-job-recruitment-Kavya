from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile
from django.contrib.auth.models import User


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    location = forms.CharField(max_length=100)
    
    USER_TYPE_CHOICES = [
        ('job_seeker','Job Seeker'),
        ('employer','Employer'),
    ]
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,  # <- THIS IS KEY
    )

    class Meta:
        model = User
        fields = ['user_type', 'username', 'email', 'phone', 'location', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError("Resume must be a PDF")
        return resume
