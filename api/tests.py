from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from rest_framework import status
from .models import Categoria, Proveedor, Producto, MovimientoInventario


class AuthAndProtectedViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.categoria = Categoria.objects.create(nombre='Herramientas', descripcion='Ferretería')
        self.proveedor = Proveedor.objects.create(
            rut='76123456-7',
            razon_social='Ferretería Central SpA',
            contacto_email='ventas@ferreteria.cl',
            telefono='+56911223344'
        )
        self.producto = Producto.objects.create(
            sku='TAL-750W',
            nombre='Taladro Percutor 750W',
            categoria=self.categoria,
            proveedor=self.proveedor,
            precio_unitario=Decimal('45990.00'),
            stock_actual=10,
            stock_minimo=3
        )

    def test_dashboard_redirects_anonymous_user(self):
        """dashboard/ sin autenticación debe redirigir con 302 a /login/?next=/dashboard/"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertIn('next=/dashboard/', response.url)

    def test_inventario_redirects_anonymous_user(self):
        """inventario/ sin autenticación debe redirigir con 302 a /login/?next=/inventario/"""
        response = self.client.get('/inventario/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertIn('next=/inventario/', response.url)

    def test_dashboard_accessible_when_authenticated(self):
        """dashboard/ accesible con 200 tras login"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Indicadores de Inventario')

    def test_inventario_accessible_when_authenticated(self):
        """inventario/ accesible con 200 tras login"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get('/inventario/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Taladro Percutor 750W')

    def test_api_endpoints_respond_json(self):
        """Verificar los 4 endpoints REST: categorias, proveedores, productos, movimientos"""
        # Categorías
        res_cat = self.client.get('/api/categorias/')
        self.assertEqual(res_cat.status_code, status.HTTP_200_OK)

        # Proveedores
        res_prov = self.client.get('/api/proveedores/')
        self.assertEqual(res_prov.status_code, status.HTTP_200_OK)

        # Productos
        res_prod = self.client.get('/api/productos/')
        self.assertEqual(res_prod.status_code, status.HTTP_200_OK)

        # Movimientos (requiere autenticación para crear)
        self.client.login(username='testuser', password='password123')
        res_mov = self.client.post('/api/movimientos/', {
            'producto': self.producto.id,
            'tipo_movimiento': 'ENTRADA',
            'cantidad': 5,
            'motivo': 'Recepción inicial bodega'
        }, content_type='application/json')
        self.assertEqual(res_mov.status_code, status.HTTP_201_CREATED)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_actual, 15)
