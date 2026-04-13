# 🧪 Django Shell Demonstration – MediCare

```python
# Start shell using: python manage.py shell

from django.contrib.auth.models import User
from appointments.models import UserProfile, Doctor, Appointment
from datetime import date, time

# Create Users
patient = User.objects.create_user(username='john', password='1234', first_name='John', last_name='Doe')
doctor_user = User.objects.create_user(username='drsmith', password='1234', first_name='Smith', last_name='Williams')

# Create Profiles
patient_profile = UserProfile.objects.create(user=patient, role='patient', phone='9876543210', address='Bangalore')
doctor_profile = UserProfile.objects.create(user=doctor_user, role='doctor', phone='9123456780', address='Mangalore')

# Create Doctor
doctor = Doctor.objects.create(user=doctor_user, specialization='Cardiologist', experience_years=10, consultation_fee=500, available_from=time(9, 0), available_to=time(17, 0), bio='Experienced heart specialist')

# Create Appointment
appointment = Appointment.objects.create(patient=patient, doctor=doctor, appointment_date=date.today(), appointment_time=time(10, 30), reason='Chest pain')

# Basic Queries
Doctor.objects.all()
UserProfile.objects.all()
Appointment.objects.all()

# Filters
Appointment.objects.filter(patient=patient)
Appointment.objects.filter(doctor=doctor)
Appointment.objects.filter(status='pending')
Doctor.objects.filter(specialization='Cardiologist')

# Get single object
Appointment.objects.get(id=appointment.id)

# Update
appointment.status = 'confirmed'
appointment.save()

appointment.notes = 'Patient needs ECG'
appointment.status = 'completed'
appointment.save()

# Relationship Access
patient.profile
doctor_user.doctor_profile
appointment.doctor.user.get_full_name()
appointment.patient.username

# Reverse Relations
doctor.doctor_appointments.all()
patient.patient_appointments.all()

# Aggregations
Appointment.objects.count()
Appointment.objects.filter(doctor=doctor).count()
Appointment.objects.filter(appointment_date=date.today())

# Ordering (as per Meta)
Appointment.objects.all()

# Availability Check
Doctor.objects.filter(is_available=True)

# Update Doctor Availability
doctor.is_available = False
doctor.save()

# Safe Query (avoid crash)
Appointment.objects.filter(id=999).exists()

# Delete
appointment.delete()

# Optional Cleanup
patient.delete()
doctor_user.delete()
```
