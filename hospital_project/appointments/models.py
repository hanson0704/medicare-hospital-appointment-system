from django.db import models
from django.contrib.auth.models import User

SPECIALIZATION_CHOICES = [
    ('Cardiologist', 'Cardiologist'),
    ('Dermatologist', 'Dermatologist'),
    ('Neurologist', 'Neurologist'),
    ('Orthopedic', 'Orthopedic'),
    ('Pediatrician', 'Pediatrician'),
    ('Psychiatrist', 'Psychiatrist'),
    ('Dentist', 'Dentist'),
    ('General Physician', 'General Physician'),
]

ROLE_CHOICES = [
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
]


# 1. USER PROFILE MODEL
class UserProfile(models.Model):
    """
    Extends the default Django User model.
    Every user (patient or doctor) has a profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# 2. DOCTOR MODEL
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    available_from = models.TimeField(default='09:00')
    available_to = models.TimeField(default='17:00')
    bio = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"


# 3. APPOINTMENT MODEL
class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)  # Doctor's notes after visit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.patient.username} → Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"