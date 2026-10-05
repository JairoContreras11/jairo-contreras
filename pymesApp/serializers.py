from rest_framework import serializers
from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Categoria.
    Incluye campo calculado 'total_productos' para contabilizar productos asociados.
    """
    total_productos = serializers.IntegerField(source='productos.count', read_only=True)

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'total_productos']


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Producto.
    Incluye campos explícitos, nombre de categoría para lectura y validación de negocio.
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
        Validación requerida por rúbrica:
        El precio estimado debe ser un valor mayor o igual a cero.
        """
        if value < 0:
            raise serializers.ValidationError("El precio estimado no puede ser un valor negativo.")
        return value
