from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def _str_(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    def _str_(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)

    def _str_(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, related_name="productos"
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos"
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.nombre

    @property
    def stock_bajo(self):
        return self.stock < self.stock_minimo


class MovimientoInventario(models.Model):
    ENTRADA = "entrada"
    SALIDA = "salida"
    TIPO_CHOICES = [
        (ENTRADA, "Entrada"),
        (SALIDA, "Salida"),
    ]

    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="movimientos"
    )
    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, null=True, blank=True
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.CharField(max_length=200, blank=True)

    def _str_(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

    def save(self, *args, **kwargs):
        # Actualiza el stock del producto según el tipo de movimiento.
        # kwargs['raw'] es True cuando los datos vienen de un fixture
        # (loaddata); en ese caso el stock ya viene correcto en el JSON
        # y no debe recalcularse.
        es_carga_de_fixture = kwargs.get("raw", False)
        if self.pk is None and not es_carga_de_fixture:
            if self.tipo == self.ENTRADA:
                self.producto.stock += self.cantidad
            elif self.tipo == self.SALIDA:
                self.producto.stock -= self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)