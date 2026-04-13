from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Doctor, Appointment
from .forms import RegisterForm, LoginForm, AppointmentForm, ProfileEditForm, DoctorProfileEditForm

def patient_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.profile.role != 'patient':
            messages.error(request, "Only patients can book appointments.")
            return redirect('home')  # or doctor_dashboard
        return view_func(request, *args, **kwargs)
    return wrapper

# HOME
def home(request):
    doctors = Doctor.objects.filter(is_available=True)[:6]
    return render(request, 'home.html', {'doctors': doctors})


# REGISTER
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            phone = form.cleaned_data.get('phone')

            # Create UserProfile
            UserProfile.objects.create(user=user, role=role, phone=phone)

            # If doctor role, create empty Doctor profile
            if role == 'doctor':
                Doctor.objects.create(user=user, specialization='General Physician')

            messages.success(request, f'Account created successfully! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'register.html', {'form': form})


# LOGIN
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')

                # Redirect based on role
                try:
                    role = user.profile.role
                    if role == 'doctor':
                        return redirect('doctor_dashboard')
                    else:
                        return redirect('patient_dashboard')
                except UserProfile.DoesNotExist:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})


# LOGOUT
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# PATIENT DASHBOARD
@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user)
    doctors = Doctor.objects.filter(is_available=True)
    context = {
        'appointments': appointments,
        'doctors': doctors,
        'total': appointments.count(),
        'pending': appointments.filter(status='pending').count(),
        'confirmed': appointments.filter(status='confirmed').count(),
        'cancelled': appointments.filter(status='cancelled').count(),
    }
    return render(request, 'patient_dashboard.html', context)


# DOCTOR DASHBOARD
@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor_profile
        appointments = Appointment.objects.filter(doctor=doctor)
        context = {
            'appointments': appointments,
            'doctor': doctor,
            'total': appointments.count(),
            'pending': appointments.filter(status='pending').count(),
            'confirmed': appointments.filter(status='confirmed').count(),
            'completed': appointments.filter(status='completed').count(),
        }
        return render(request, 'doctor_dashboard.html', context)
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('home')


# BOOK APPOINTMENT
@login_required
@patient_required
def book_appointment(request, doctor_id):

    doctor = get_object_or_404(Doctor, id=doctor_id)
    form = AppointmentForm()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient_dashboard')

    return render(request, 'book_appointment.html', {
        'form': form,
        'doctor': doctor
    })


# UPDATE APPOINTMENT STATUS (Doctor)
@login_required
def update_appointment(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = status
    appointment.save()
    messages.success(request, f'Appointment marked as {status}.')
    return redirect('doctor_dashboard')


# CANCEL APPOINTMENT (Patient)
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, 'Appointment cancelled.')
    return redirect('patient_dashboard')

# ─────────────────────────────────────────
# EDIT PROFILE
# ─────────────────────────────────────────
@login_required
def edit_profile(request):
    profile = request.user.profile
    is_doctor = profile.role == 'doctor'

    user_form = ProfileEditForm(instance=profile)
    user_form.fields['first_name'].initial = request.user.first_name
    user_form.fields['last_name'].initial = request.user.last_name
    user_form.fields['email'].initial = request.user.email

    doctor_form = DoctorProfileEditForm(
        instance=request.user.doctor_profile if is_doctor else None
    ) if is_doctor else None

    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=profile)
        user_form.fields['first_name'].initial = request.user.first_name
        user_form.fields['last_name'].initial = request.user.last_name
        user_form.fields['email'].initial = request.user.email

        if is_doctor:
            doctor_form = DoctorProfileEditForm(request.POST, instance=request.user.doctor_profile)

        if user_form.is_valid() and (not is_doctor or doctor_form.is_valid()):
            # Save User fields
            request.user.first_name = user_form.cleaned_data['first_name']
            request.user.last_name = user_form.cleaned_data['last_name']
            request.user.email = user_form.cleaned_data['email']
            request.user.save()

            # Save Profile fields
            user_form.save()

            # Save Doctor fields
            if is_doctor:
                doctor_form.save()

            messages.success(request, 'Profile updated successfully! ✅')
            if is_doctor:
                return redirect('doctor_dashboard')
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'doctor_form': doctor_form,
        'is_doctor': is_doctor,
    })