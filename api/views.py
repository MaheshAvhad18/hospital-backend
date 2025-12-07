from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Count
from datetime import datetime, timedelta

from .models import Hospital, Doctor, Appointment
from .serializers import HospitalSerializer, DoctorSerializer, AppointmentSerializer


# -----------------------------
# 1. List all hospitals
# -----------------------------
class HospitalListAPI(APIView):
    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)


# -----------------------------
# 2. List doctors for one hospital
# -----------------------------
class HospitalDoctorsAPI(APIView):
    def get(self, request, hospital_id):
        doctors = Doctor.objects.filter(hospital_id=hospital_id)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


# -----------------------------
# 3. Doctor availability by date
# -----------------------------
class DoctorAvailabilityAPI(APIView):
    def get(self, request, doctor_id):
        date_str = request.GET.get("date")
        if not date_str:
            return Response({"error": "date=YYYY-MM-DD is required"}, status=400)

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        doctor = Doctor.objects.get(id=doctor_id)

        # Slot length = 10 mins
        slot_duration = timedelta(minutes=10)

        start = datetime.combine(date, doctor.available_from)
        end = datetime.combine(date, doctor.available_to)

        slots = []
        current = start

        booked_slots = Appointment.objects.filter(doctor=doctor, date=date).values_list("time", flat=True)

        while current <= end:
            slot_time = current.time()
            if slot_time not in booked_slots:
                slots.append(slot_time.strftime("%H:%M"))
            current += slot_duration

        return Response({
            "doctor": doctor.name,
            "date": date_str,
            "available_slots": slots
        })


# -----------------------------
# 4. Book an appointment
# -----------------------------
class BookAppointmentAPI(APIView):
    def post(self, request):

        doctor_id = request.data.get("doctor_id")
        date_str = request.data.get("date")
        time_str = request.data.get("time")
        patient_name = request.data.get("patient_name")
        patient_phone = request.data.get("patient_phone")

        if not all([doctor_id, date_str, time_str, patient_name, patient_phone]):
            return Response({"error": "Missing required fields"}, status=400)

        doctor = Doctor.objects.get(id=doctor_id)
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()

        # Check if slot is free
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            return Response({"error": "Slot not available"}, status=409)

        # Token logic = count existing + 1
        token = Appointment.objects.filter(doctor=doctor, date=date).count() + 1

        appointment = Appointment.objects.create(
            patient_name=patient_name,
            patient_phone=patient_phone,
            doctor=doctor,
            date=date,
            time=time,
            token_number=token
        )

        serializer = AppointmentSerializer(appointment)
        return Response({
            "message": "Appointment booked successfully",
            "token": token,
            "data": serializer.data
        }, status=201)

