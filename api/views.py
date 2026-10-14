from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Sum, F
from rest_framework import viewsets, permissions
from .models import Categoria, Proveedor, Producto, MovimientoInventario
from .serializers import (
    CategoriaSerializer, 
    ProveedorSerializer, 
    ProductoSerializer, 
    MovimientoInventarioSerializer
)

# 1. Vista Pública
def bienvenida(request):
    return render(request, 'bienvenida.html')

# 2. FBV Protegida (@login_required) con KPIs de Negocio
@login_required
def dashboard_privado(request):
    total_productos = Producto.objects.count()
    productos_criticos = Producto.objects.filter(stock_actual__lte=F('stock_minimo')).count()
    valor_inventario = Producto.objects.aggregate(
        total=Sum(F('stock_actual') * F('precio_unitario'))
    )['total'] or 0
    
    ultimos_movimientos = MovimientoInventario.objects.select_related(
        'producto', 'usuario'
    ).order_by('-fecha_registro')[:6]

    contexto = {
        'usuario': request.user,
        'total_productos': total_productos,
        'productos_criticos': productos_criticos,
        'valor_inventario': valor_inventario,
        'ultimos_movimientos': ultimos_movimientos,
    }
    return render(request, 'dashboard.html', contexto)

# 3. CBV Protegida (LoginRequiredMixin)
class GestionProductosPrivadaView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'gestion_productos.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        return Producto.objects.select_related('categoria', 'proveedor').order_by('nombre')

# 4. ViewSets de API REST
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('categoria', 'proveedor').all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.select_related('producto', 'usuario').all()
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
