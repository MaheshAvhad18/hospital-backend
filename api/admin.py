from django.contrib import admin
from .models import Hospital, Doctor, StaffProfile, Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "doctor", "date", "time", "token_number")

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superuser sees all
        if request.user.is_superuser:
            return qs

        # Check for staff profile
        try:
            staff = StaffProfile.objects.get(user=request.user)
        except StaffProfile.DoesNotExist:
            return qs.none()

        # Reception & SuperAdmin: see only their hospital's appointments
        if staff.role in ["superadmin", "reception"]:
            return qs.filter(doctor__hospital=staff.hospital)

        # Doctor: see only their appointments
        if staff.role == "doctor":
            doctor = Doctor.objects.get(user=request.user)
            return qs.filter(doctor=doctor)

        return qs.none()


admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(StaffProfile)
admin.site.register(Appointment, AppointmentAdmin)
