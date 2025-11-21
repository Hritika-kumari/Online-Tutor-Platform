from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutor_list, name='tutor_list'),
    path('<int:tutor_id>/', views.tutor_detail, name='tutor_detail'),
    path('dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('subject/add/', views.add_subject, name='add_subject'),
    path('availability/add/', views.add_availability, name='add_availability'),
]

