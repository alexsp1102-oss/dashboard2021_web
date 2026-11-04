from django.contrib import admin
from .models import Venta, DetalleVenta

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'cliente', 'sucursal', 'vendedor', 'metodo_pago', 'calcular_total')
    inlines = [DetalleVentaInline]

    def calcular_total(self, obj):
        return sum(detalle.cantidad * detalle.precio_unitario for detalle in obj.detalles.all())
    calcular_total.short_description = "Total"

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'precio_unitario', 'calcular_importe')

    def calcular_importe(self, obj):
        return obj.cantidad * obj.precio_unitario
    calcular_importe.short_description = "Importe"


# Register your models here.
