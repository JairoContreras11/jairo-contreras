"""
Vistas basadas en ModelViewSet para la app api según rúbrica de evaluación.
"""
from rest_framework import viewsets
from pymesApp.models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet que provee acciones completas CRUD para Categorías.
    """
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet que provee acciones completas CRUD para Productos.
    """
    queryset = Producto.objects.all().select_related('categoria').order_by('id')
    serializer_class = ProductoSerializer
