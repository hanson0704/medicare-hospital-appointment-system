from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Doctor, Appointment


# REGISTRATION FORM
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    role = forms.ChoiceField(
        choices=[('patient', 'Patient'), ('doctor', 'Doctor')],
        widget=forms.Select()
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# LOGIN FORM
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
    )


# APPOINTMENT BOOKING FORM
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'reason']
        widgets = {
            'appointment_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'appointment_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'reason': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your symptoms or reason for visit...',
                'class': 'form-control'
            }),
        }
        

# PROFILE EDIT FORM
class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Your address...',
                'class': 'form-control',
                'rows': 3
            }),
        }


# DOCTOR PROFILE EDIT FORM
class DoctorProfileEditForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'experience_years', 'consultation_fee', 'available_from', 'available_to', 'bio', 'is_available']
        widgets = {
            'specialization': forms.Select(attrs={'class': 'form-select'}),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience'
            }),
            'consultation_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fee in ₹'
            }),
            'available_from': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'available_to': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a short bio...',
                'rows': 3
            }),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }