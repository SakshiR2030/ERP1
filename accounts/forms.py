from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, ConcessionApplication


# Registration form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "full_name", "password1", "password2"]

# Login form
class StudentLoginForm(forms.Form):
    username = forms.CharField(label="College ID", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Student profile form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["full_name", "branch", "year"]  # ✅ Only keep the actual fields from Student


class ConcessionApplicationForm(forms.ModelForm):
    """
    Form to handle the ConcessionApplication model.
    This form will be used to collect the concession details.
    """
    class Meta:
        model = ConcessionApplication
        fields = ['class_type', 'period', 'line', 'from_station', 'to_station']
        widgets = {
            'class_type': forms.Select(attrs={'class': 'form-control'}),
            'period': forms.Select(attrs={'class': 'form-control'}),
            'line': forms.Select(attrs={'class': 'form-control', 'onchange': 'updateStations()'}),
            'from_station': forms.Select(attrs={'class': 'form-control'}),
            'to_station': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial empty choices for from_station (will be populated by JavaScript)
        self.fields['from_station'].choices = [('', 'Select Station')]
        # Set default value for to_station
        self.fields['to_station'].initial = 'Wadala'
