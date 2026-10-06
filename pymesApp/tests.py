from django.test import TestCase
from django.db.models.deletion import ProtectedError
from rest_framework.test import APIClient
from rest_framework import status
from .models import Categoria, Producto


class ModelsTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Bebidas",
            descripcion="Bebidas y refrescos"
        )
        self.producto = Producto.objects.create(
            nombre="Agua Mineral 1.5L",
            categoria=self.categoria,
            precio_estimado=1200.00,
            stock=20,
            stock_minimo=5
        )

    def test_categoria_str(self):
        self.assertEqual(str(self.categoria), "Bebidas")

    def test_producto_str(self):
        self.assertIn("Agua Mineral 1.5L", str(self.producto))

    def test_categoria_protect_on_delete(self):
        """Verifica que la regla on_delete=models.PROTECT impida borrar una categoría con productos"""
        with self.assertRaises(ProtectedError):
            self.categoria.delete()


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.categoria = Categoria.objects.create(
            nombre="Limpieza",
            descripcion="Artículos de aseo"
        )

    def test_categoria_crud(self):
        # 1. GET lista
        res_list = self.client.get('/api/categorias/')
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)

        # 2. POST crear
        res_post = self.client.post('/api/categorias/', {
            'nombre': 'Lácteos',
            'descripcion': 'Leche, quesos, yogur'
        }, format='json')
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        new_cat_id = res_post.data['id']

        # 3. GET detalle
        res_det = self.client.get(f'/api/categorias/{new_cat_id}/')
        self.assertEqual(res_det.status_code, status.HTTP_200_OK)
        self.assertEqual(res_det.data['nombre'], 'Lácteos')

        # 4. DELETE eliminar
        res_del = self.client.delete(f'/api/categorias/{new_cat_id}/')
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)

    def test_producto_crud_and_validations(self):
        # 1. POST producto válido
        res_post = self.client.post('/api/productos/', {
            'nombre': 'Detergente 3L',
            'descripcion': 'Detergente líquido',
            'precio_estimado': 4990.00,
            'stock': 15,
            'stock_minimo': 3,
            'disponible': True,
            'categoria': self.categoria.id
        }, format='json')
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        prod_id = res_post.data['id']

        # 2. GET detalle
        res_det = self.client.get(f'/api/productos/{prod_id}/')
        self.assertEqual(res_det.status_code, status.HTTP_200_OK)

        # 3. PATCH modificar stock
        res_patch = self.client.patch(f'/api/productos/{prod_id}/', {'stock': 25}, format='json')
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(res_patch.data['stock'], 25)

        # 4. DELETE eliminar
        res_del = self.client.delete(f'/api/productos/{prod_id}/')
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)

    def test_validacion_precio_estimado_negativo(self):
        """Verifica que validate_precio_estimado rechace valores < 0 con HTTP 400"""
        res = self.client.post('/api/productos/', {
            'nombre': 'Producto Inválido',
            'precio_estimado': -250.00,
            'categoria': self.categoria.id
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('precio_estimado', res.data)
