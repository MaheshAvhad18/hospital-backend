from django.urls import path
from .views import (
    HospitalListAPI, HospitalDoctorsAPI,
    DoctorAvailabilityAPI, BookAppointmentAPI
)

urlpatterns = [
    path("hospitals/", HospitalListAPI.as_view()),
    path("hospitals/<int:hospital_id>/doctors/", HospitalDoctorsAPI.as_view()),
    path("doctors/<int:doctor_id>/availability/", DoctorAvailabilityAPI.as_view()),
    path("book-appointment/", BookAppointmentAPI.as_view()),
]
