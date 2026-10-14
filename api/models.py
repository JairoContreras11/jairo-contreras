from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    razon_social = models.CharField(max_length=150)
    contacto_email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['razon_social']

    def __str__(self):
        return f"{self.razon_social} ({self.rut})"


class Producto(models.Model):
    sku = models.CharField(max_length=30, unique=True, verbose_name="Código SKU")
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='productos')
    precio_unitario = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return f"[{self.sku}] {self.nombre}"

    @property
    def alerta_stock(self):
        return self.stock_actual <= self.stock_minimo


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Recepción de Mercadería'),
        ('SALIDA', 'Despacho o Venta'),
        ('AJUSTE', 'Ajuste de Auditoría'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='movimientos_registrados')
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    stock_resultante = models.PositiveIntegerField()
    motivo = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} ({self.cantidad} un.)"
