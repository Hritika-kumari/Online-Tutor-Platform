from django.urls import path
from . import views

urlpatterns = [
    path('', views.material_list, name='material_list'),
    path('upload/', views.upload_material, name='upload_material'),
]

