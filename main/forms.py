from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Report

class PatientForm(forms.ModelForm):
    # Add the imagerie field separately since it's not part of the Patient model
    imagerie = forms.ImageField(
        label="Medical Scan/Image",
        help_text="Upload the medical scan or image for this report",
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'cin', 'mail', 'reference_dossier']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'cin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CIN'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'reference_dossier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Référence Dossier'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'cin', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'cin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CIN'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': True}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required for password reset link.")
        return email

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['text', 'imagerie']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 10,
                'placeholder': 'Enter report text here...'
            }),
            'imagerie': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
