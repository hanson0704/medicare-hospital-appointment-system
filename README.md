# 🏥 MediCare – Hospital Appointment System

## 📌 Overview

MediCare is a web-based hospital appointment management system built using Django. It allows patients to book appointments with doctors while enabling doctors to manage schedules and appointments efficiently. The system uses role-based authentication to ensure secure and structured interaction between patients and doctors.

---

## 🚀 Features

### 👤 Authentication & Roles

- User Registration (Patient / Doctor)
- Secure Login & Logout system
- Role-based access control

### 🩺 Doctor Module

- Doctor profile creation and management
- Set specialization, experience, and consultation fee
- Define availability timings
- View and manage patient appointments
- Update appointment status (Pending, Confirmed, Completed, Cancelled)

### 🧑‍💼 Patient Module

- Browse available doctors
- Book appointments easily
- View appointment history
- Cancel appointments

### 📊 Dashboard System

- Patient Dashboard – View and manage appointments
- Doctor Dashboard – Manage patient bookings

### 🎨 UI/UX

- Modern glassmorphism UI
- Responsive design using Bootstrap
- Clean and user-friendly interface

---

## 🛠️ Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap 5
- Database: SQLite
- Authentication: Django Auth System

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hanson0704/medicare-hospital-appointment-system.git
cd medicare-hospital-appointment-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
cd hospital_project
python manage.py makemigrations
python manage.py migrate
```

### 5. Run Server

```bash
python manage.py runserver
```

### 6. Open in Browser

http://127.0.0.1:8000/

---

## 📷 Screenshots

Add your screenshots inside a `screenshots` folder.

- Home Page → screenshots/home.png
- Register Page → screenshots/register.png
- Patient Dashboard → screenshots/patient_dashboard.png
- Doctor Dashboard → screenshots/doctor_dashboard.png
- Booking Page → screenshots/booking.png

---

## 📁 Project Structure

```
hospital_project/
│── appointments/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│
│── hospital_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
│── profile_pics/
│
│── static/
│   ├── css/
│   │   └── style.css
│
│── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── patient_dashboard.html
│   ├── doctor_dashboard.html
│   ├── book_appointment.html
│   ├── edit_profile.html
│
│── db.sqlite3
│── manage.py
```

---

## 🔐 Security & Access Control

- Role-based restrictions implemented:
  - Doctors cannot book appointments
  - Only patients can book appointments
- Protected routes using login_required and custom role-based decorators

---

## 🌟 Unique Highlights

- Clean role-based system using UserProfile
- Custom decorators for access control
- Smooth UI with glass-card design
- Real-world doctor-patient workflow simulation

---

## 🚧 Future Enhancements

- Payment integration (Razorpay / Stripe)
- Email/SMS notifications
- Doctor rating & review system
- Admin analytics dashboard
- Slot-based booking system

---

## 👨‍💻 Authors

- Hanson Vaz
- Anush

---

## 📄 License

This project is developed for educational purposes (MCA Project).
