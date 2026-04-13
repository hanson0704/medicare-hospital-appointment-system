from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Doctor, Appointment


# INLINE — Show UserProfile inside User Admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# CUSTOM USER ADMIN
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_select_related = ('profile',)

    def get_role(self, instance):
        try:
            return instance.profile.role.capitalize()
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'


# DOCTOR ADMIN
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',
        'specialization',
        'experience_years',
        'consultation_fee',
        'available_from',
        'available_to',
        'is_available',
    )
    list_filter = ('specialization', 'is_available')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    list_editable = ('is_available',)

    def get_full_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    get_full_name.short_description = 'Doctor Name'


# APPOINTMENT ADMIN
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'get_patient_name',
        'get_doctor_name',
        'appointment_date',
        'appointment_time',
        'status',
        'created_at',
    )
    list_filter = ('status', 'appointment_date', 'doctor__specialization')
    search_fields = ('patient__username', 'doctor__user__first_name', 'reason')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')

    def get_patient_name(self, obj):
        return obj.patient.get_full_name() or obj.patient.username
    get_patient_name.short_description = 'Patient'

    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'


# USERPROFILE ADMIN
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'phone')


# RE-REGISTER USER WITH CUSTOM ADMIN
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ADMIN SITE BRANDING
admin.site.site_header = "🏥 Hospital Management Admin"
admin.site.site_title = "Hospital Admin Portal"
admin.site.index_title = "Welcome to Hospital Management System"