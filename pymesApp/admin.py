from django.contrib import admin
from .models import Categoria, Proveedor, Cliente, Producto, MovimientoInventario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rut", "telefono", "correo")
    search_fields = ("nombre", "rut")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rut", "telefono", "correo")
    search_fields = ("nombre", "rut")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "proveedor", "precio", "stock", "stock_bajo")
    list_filter = ("categoria", "proveedor")
    search_fields = ("nombre",)


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ("producto", "tipo", "cantidad", "cliente", "fecha")
    list_filter = ("tipo", "fecha")
    search_fields = ("producto__nombre",)