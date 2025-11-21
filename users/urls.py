from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/student/', views.student_profile, name='student_profile'),
    path('profile/tutor/', views.tutor_profile, name='tutor_profile'),
    path('profile/student/edit/', views.edit_student_profile, name='edit_student_profile'),
    path('profile/tutor/edit/', views.edit_tutor_profile, name='edit_tutor_profile'),
]

