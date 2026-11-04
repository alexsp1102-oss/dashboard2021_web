from django.core.management.base import BaseCommand
from openpyxl import load_workbook
from datetime import datetime
from decimal import Decimal
import os

from catalogos.models import Categoria, Sucursal, MetodoPago, Cliente, Vendedor, Producto
from ventas.models import Venta, DetalleVenta


class Command(BaseCommand):
    help = 'Importa datos desde Excel'

    def add_arguments(self, parser):
        parser.add_argument('--archivo', type=str, required=True)

    def handle(self, *args, **options):

        archivo = options['archivo']

        if not os.path.exists(archivo):
            self.stdout.write(self.style.ERROR("Archivo no encontrado"))
            return

        wb = load_workbook(archivo)
        ws = wb['BaseDeDatos']

        filas = list(ws.iter_rows(values_only=True))

        encabezados = [str(h).strip().lower() for h in filas[0]]

        for fila in filas[1:]:

            datos = dict(zip(encabezados, fila))

            try:

                fecha = datos.get('fecha')

                if isinstance(fecha, datetime):
                    fecha = fecha.date()
                else:
                    fecha = datetime.today().date()

                cliente_nombre = str(datos.get('cliente', '')).strip()
                vendedor_nombre = str(datos.get('vendedor', '')).strip()
                sucursal_nombre = str(datos.get('empresa', '')).strip()
                metodo_pago_nombre = str(datos.get('forma de pago', '')).strip()
                producto_nombre = str(datos.get('producto', '')).strip()
                categoria_nombre = str(datos.get('categoría', '')).strip()

                precio = Decimal(str(datos.get('precio_unitario', 0) or 0))
                cantidad = Decimal(str(datos.get('cantidad', 0) or 0))
                importe = Decimal(str(datos.get('importe', 0) or 0))

                categoria, _ = Categoria.objects.get_or_create(nombre=categoria_nombre)

                sucursal, _ = Sucursal.objects.get_or_create(nombre=sucursal_nombre)

                metodo_pago, _ = MetodoPago.objects.get_or_create(nombre=metodo_pago_nombre)

                cliente, _ = Cliente.objects.get_or_create(nombre=cliente_nombre)

                vendedor, _ = Vendedor.objects.get_or_create(nombre=vendedor_nombre)

                producto, _ = Producto.objects.get_or_create(
                    nombre=producto_nombre,
                    defaults={'categoria': categoria, 'precio': precio}
                )

                venta = Venta.objects.create(
                    fecha=fecha,
                    cliente=cliente,
                    sucursal=sucursal,
                    vendedor=vendedor,
                    metodo_pago=metodo_pago,
                    subtotal=importe,
                    impuesto=importe * Decimal("0.16"),
                    total=importe * Decimal("1.16")
                )

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    importe=importe
                )

            except Exception as e:
                print("Error en fila:", e)

        self.stdout.write(self.style.SUCCESS("Importación terminada"))