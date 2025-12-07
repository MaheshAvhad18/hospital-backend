from django.contrib import admin
from .models import Hospital, Doctor, StaffProfile, Appointment

admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(StaffProfile)
admin.site.register(Appointment)
