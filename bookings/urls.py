from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:tutor_id>/', views.create_booking, name='create_booking'),
    path('update/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]

