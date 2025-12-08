from django.db import models
from django.contrib.auth.models import User , Group

# -----------------------------
# Hospital Model
# -----------------------------
class Hospital(models.Model):
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -----------------------------
# Doctor Model
# -----------------------------
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)

    available_from = models.TimeField()
    available_to = models.TimeField()

    status = models.BooleanField(default=True)  # active/inactive doctor

    def __str__(self):
        return f"{self.name} ({self.specialization})"


# -----------------------------
# Staff Profile (Reception + Super Admin for each hospital)
# -----------------------------

class StaffProfile(models.Model):
    ROLE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("reception", "Reception Staff"),
        ("doctor", "Doctor"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        role_to_group = {
            "superadmin": "SuperAdmin",
            "reception": "Reception",
            "doctor": "Doctor",
        }

        group_name = role_to_group.get(self.role)

        if group_name:
            group = Group.objects.get(name=group_name)

            # remove old roles
            self.user.groups.clear()
            # assign correct role
            self.user.groups.add(group)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# -----------------------------
# Appointment Model
# -----------------------------
class Appointment(models.Model):
    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=20)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    token_number = models.IntegerField()

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name} ({self.date})"
