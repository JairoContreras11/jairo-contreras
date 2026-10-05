"""
Serializadores DRF para la app api según rúbrica de evaluación.
"""
from rest_framework import serializers
from pymesApp.models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializador para Categoria con cálculo de productos asociados.
    """
    total_productos = serializers.IntegerField(source='productos.count', read_only=True)

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'total_productos']


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador para Producto con validación de precio estimado.
    """
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio_estimado',
            'stock',
            'stock_minimo',
            'disponible',
            'categoria',
            'categoria_nombre',
            'proveedor',
            'fecha_creacion'
        ]

    def validate_precio_estimado(self, value):
        """
        Validación requerida por la rúbrica docente:
        No se permiten valores negativos en el precio estimado.
        """
        if value < 0:
            raise serializers.ValidationError("El precio estimado no puede ser un valor negativo.")
        return value
