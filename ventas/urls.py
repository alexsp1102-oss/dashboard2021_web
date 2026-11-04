from django.urls import path
from .views import index, lista_ventas

urlpatterns = [
    path('', index, name='ventas_index'),
    path('ventas/', lista_ventas, name='lista_ventas'),
]
