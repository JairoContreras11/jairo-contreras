from django.contrib import admin
from .models import Categoria, Proveedor, Producto, MovimientoInventario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'rut', 'telefono', 'contacto_email', 'activo')
    list_filter = ('activo',)
    search_fields = ('razon_social', 'rut')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'categoria', 'proveedor', 'precio_unitario', 'stock_actual', 'alerta_stock', 'activo')
    list_filter = ('categoria', 'proveedor', 'activo')
    search_fields = ('sku', 'nombre')


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo_movimiento', 'cantidad', 'stock_resultante', 'usuario', 'fecha_registro')
    list_filter = ('tipo_movimiento', 'fecha_registro')
    search_fields = ('producto__nombre', 'motivo', 'usuario__username')
