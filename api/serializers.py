from rest_framework import serializers
from .models import Hospital, Doctor, Appointment

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source="hospital.name", read_only=True)

    class Meta:
        model = Doctor
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
