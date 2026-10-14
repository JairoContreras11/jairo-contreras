from rest_framework import serializers
from .models import Categoria, Proveedor, Producto, MovimientoInventario


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    alerta_stock = serializers.ReadOnlyField()
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.razon_social')

    class Meta:
        model = Producto
        fields = [
            'id', 'sku', 'nombre', 'categoria', 'categoria_nombre',
            'proveedor', 'proveedor_nombre', 'precio_unitario',
            'stock_actual', 'stock_minimo', 'alerta_stock', 'activo'
        ]

    def validate_precio_unitario(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio del producto debe ser mayor a 0.")
        return value

    def validate(self, data):
        stock = data.get('stock_actual', getattr(self.instance, 'stock_actual', 0))
        stock_min = data.get('stock_minimo', getattr(self.instance, 'stock_minimo', 0))
        if stock < 0 or stock_min < 0:
            raise serializers.ValidationError("Los valores de stock no pueden ser negativos.")
        return data


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    usuario_username = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = MovimientoInventario
        fields = [
            'id', 'producto', 'producto_nombre', 'usuario', 'usuario_username',
            'tipo_movimiento', 'cantidad', 'stock_resultante', 'motivo', 'fecha_registro'
        ]
        read_only_fields = ['stock_resultante', 'usuario', 'fecha_registro']

    def create(self, validated_data):
        producto = validated_data['producto']
        tipo = validated_data['tipo_movimiento']
        cantidad = validated_data['cantidad']
        usuario = self.context['request'].user

        if tipo == 'SALIDA' and producto.stock_actual < cantidad:
            raise serializers.ValidationError({
                "cantidad": f"Stock insuficiente. Existen solo {producto.stock_actual} unidades disponibles."
            })

        if tipo == 'ENTRADA':
            producto.stock_actual += cantidad
        elif tipo == 'SALIDA':
            producto.stock_actual -= cantidad
        elif tipo == 'AJUSTE':
            producto.stock_actual = cantidad

        producto.save()

        movimiento = MovimientoInventario.objects.create(
            producto=producto,
            usuario=usuario,
            tipo_movimiento=tipo,
            cantidad=cantidad,
            stock_resultante=producto.stock_actual,
            motivo=validated_data['motivo']
        )
        return movimiento
