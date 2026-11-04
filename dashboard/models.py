from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    folio = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha = models.DateField()

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    metodo_pago = models.ForeignKey(
        MetodoPago,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.folio if self.folio else f"Venta {self.id}"