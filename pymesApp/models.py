from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre o Razón Social")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    correo = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    direccion = models.CharField(max_length=200, blank=True, verbose_name="Dirección")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre Completo")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    correo = models.EmailField(blank=True, verbose_name="Correo Electrónico")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
        verbose_name="Categoría"
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
        verbose_name="Proveedor"
    )
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción Detallada")
    precio_estimado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Precio Estimado"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock Disponible")
    stock_minimo = models.PositiveIntegerField(default=5, verbose_name="Stock Mínimo")
    disponible = models.BooleanField(default=True, verbose_name="¿Disponible?")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - ${self.precio_estimado}"

    # Compatibilidad con código previo que usaba 'precio'
    @property
    def precio(self):
        return self.precio_estimado

    @precio.setter
    def precio(self, valor):
        self.precio_estimado = valor

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
        Producto,
        on_delete=models.CASCADE,
        related_name="movimientos",
        verbose_name="Producto"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Cliente"
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimiento")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    observacion = models.CharField(max_length=200, blank=True, verbose_name="Observación")

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

    def save(self, *args, **kwargs):
        # Actualiza el stock del producto según el tipo de movimiento
        es_carga_de_fixture = kwargs.get("raw", False)
        if self.pk is None and not es_carga_de_fixture:
            if self.tipo == self.ENTRADA:
                self.producto.stock += self.cantidad
            elif self.tipo == self.SALIDA:
                self.producto.stock -= self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)