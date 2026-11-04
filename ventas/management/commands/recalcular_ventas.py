from django.core.management.base import BaseCommand
from ventas.models import Venta, DetalleVenta

class Command(BaseCommand):
    help = "Recalcula importes y totales de todas las ventas"

    def handle(self, *args, **kwargs):
        # Recalcular importe en cada detalle
        for d in DetalleVenta.objects.all():
            d.importe = d.cantidad * d.precio_unitario
            d.save()

        # Recalcular subtotal, impuesto y total en cada venta
        for v in Venta.objects.all():
            subtotal = sum(d.importe for d in v.detalles.all())
            v.subtotal = subtotal
            v.impuesto = subtotal * 0.16   # IVA ejemplo
            v.total = v.subtotal + v.impuesto
            v.save()

        self.stdout.write(self.style.SUCCESS("✅ Recalculo completado"))
