from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:tutor_id>/', views.add_rating, name='add_rating'),
    path('add/<int:tutor_id>/<int:booking_id>/', views.add_rating, name='add_rating_booking'),
]

