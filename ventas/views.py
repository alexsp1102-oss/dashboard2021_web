from django.http import HttpResponse
from django.shortcuts import render
from .models import Venta

def index(request):
    return HttpResponse("Bienvenido al módulo de Ventas")

def lista_ventas(request):
    # Traemos las ventas con relaciones para optimizar consultas
    ventas = Venta.objects.select_related(
        'cliente', 'sucursal', 'vendedor', 'metodo_pago'
    ).prefetch_related('detalles__producto').all().order_by('-fecha')

    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})



# Create your views here.
