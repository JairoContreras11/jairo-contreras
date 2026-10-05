from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import render
from datetime import datetime
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet para Categoria:
    Provee automáticamente operaciones CRUD completas:
    GET (lista y detalle), POST (crear), PUT (actualizar), PATCH (parcial), DELETE (eliminar).
    """
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet para Producto:
    Provee automáticamente operaciones CRUD completas:
    GET (lista y detalle), POST (crear), PUT (actualizar), PATCH (parcial), DELETE (eliminar).
    """
    queryset = Producto.objects.all().select_related('categoria').order_by('id')
    serializer_class = ProductoSerializer


def bienvenida(request):
    """
    Vista principal informativa del proyecto 'Sistema de Inventario para PYMEs'.
    """
    nombre_proyecto = "Sistema de Inventario para PYMEs"
    hora_actual = datetime.now().hour

    if hora_actual < 12:
        saludo = "Buenos dias"
    elif hora_actual < 19:
        saludo = "Buenas tardes"
    else:
        saludo = "Buenas noches"

    modulos_planificados = ["Autenticación", "Productos", "Stock", "Reportes", "API REST"]
    total_modulos = len(modulos_planificados)
    modulos_completados = 2
    avance_porcentual = round((modulos_completados / total_modulos) * 100)

    contexto = {
        "nombre_proyecto": nombre_proyecto,
        "saludo": saludo,
        "modulos_planificados": modulos_planificados,
        "total_modulos": total_modulos,
        "avance_porcentual": avance_porcentual,
    }

    return render(request, "pymesApp/bienvenida.html", contexto)
