from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.acceso_ejecutivo, name='login'),
]
