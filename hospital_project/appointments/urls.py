from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointment/update/<int:appointment_id>/<str:status>/', views.update_appointment, name='update_appointment'),
    path('appointment/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]